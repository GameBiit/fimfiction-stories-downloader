#Requires AutoHotkey v2.0
#SingleInstance Force
SetTitleMatchMode 2
SendMode "Event"
SetKeyDelay 50, 50

global browserHwnd := 0
global browserExe := ""
global downloadDir := EnvGet("USERPROFILE") "\Downloads"
global outputDir := ""
global fileFormat := "epub"
global includeAdult := false
global allPages := false
global stopRequested := false

try {
    Main()
} catch as e {
MsgBox(
    "Error: " e.Message
    . "`n`nFile: " e.File
    . "`nLine: " e.Line
    . "`n`nWhat: " e.What,
    "Fimfiction Downloader",
    "Iconx"
)
}


Main() {
    global browserHwnd, browserExe, downloadDir
    global outputDir, fileFormat, includeAdult, allPages

    promptText := "
    (
Enter parameters in the same format as the Python script:

-o downloaded_stories -a n -f epub -r 1 https://www.fimfiction.net/bookshelf/12345

Options:
-o, --out     Output folder
-a, --adult   y or n
-f, --format  txt, html, epub
-r, --range   1=current page, 2=all remaining pages

Enter the URL last.
    )"

    params := InputBox(promptText, "Fimfiction Downloader", "w650 h300")
    if (params.Result != "OK" || Trim(params.Value) = "")
        return

    parsed := ParseParameters(Trim(params.Value))

    if !parsed.Has("url") {
        MsgBox("No valid Fimfiction URL was found.")
        return
    }

    url := parsed["url"]
    outputDir := parsed.Has("out")
        ? parsed["out"]
        : A_ScriptDir "\downloaded_stories"

    adult := parsed.Has("adult") ? StrLower(parsed["adult"]) : "n"
    fileFormat := parsed.Has("format") ? StrLower(parsed["format"]) : "epub"
    rangeValue := parsed.Has("range") ? parsed["range"] : "1"

    if !(adult = "y" || adult = "n" || adult = "yes" || adult = "no") {
        MsgBox("Invalid -a value. Use y or n.")
        return
    }

    if !(fileFormat = "txt" || fileFormat = "html" || fileFormat = "epub") {
        MsgBox("Invalid -f value. Use txt, html, or epub.")
        return
    }

    if !(rangeValue = "1" || rangeValue = "2") {
        MsgBox("Invalid -r value. Use 1 or 2.")
        return
    }

    includeAdult := (adult = "y" || adult = "yes")
    allPages := (rangeValue = "2")

    MsgBox(
        "Parameters submitted.`n`n"
        . "Open Firefox or Chrome and navigate to your Fimfiction page."
        . "`nThe script will wait up to 60 seconds for a browser window.",
        "Open Browser"
    )

    browserHwnd := 0
    browserExe := ""
    startTime := A_TickCount

    while (A_TickCount - startTime < 60000) {
        ; Prefer the active browser if it is Firefox or Chrome.
        activeExe := ""
        try activeExe := WinGetProcessName("A")

        if (activeExe = "firefox.exe" || activeExe = "chrome.exe") {
            browserExe := activeExe
            browserHwnd := WinGetID("A")
            break
        }

        if WinExist("ahk_exe firefox.exe") {
            browserExe := "firefox.exe"
            browserHwnd := WinExist("ahk_exe firefox.exe")
            break
        }

        if WinExist("ahk_exe chrome.exe") {
            browserExe := "chrome.exe"
            browserHwnd := WinExist("ahk_exe chrome.exe")
            break
        }

        Sleep(500)
    }

    if !browserHwnd {
        MsgBox("No Firefox or Chrome window detected within 60 seconds.")
        return
    }

    if !DirExist(outputDir)
        DirCreate(outputDir)

    if !DirExist(downloadDir) {
        MsgBox("Downloads directory not found:`n" downloadDir)
        return
    }

    if includeAdult {
        MsgBox(
            "Make sure mature content is available in your Fimfiction session."
            . "`nPress OK to continue."
        )
    }

    pageNumber := GetPageNumber(AddQuery(url, "view_mode", "2"))
    pageURL := AddQuery(url, "view_mode", "2")
    seen := Map()
    downloaded := 0
    failed := 0

    Loop 1000 {
        if (A_Index > 1)
            pageURL := SetPageNumber(pageURL, pageNumber)

        ToolTip("Reading page " pageNumber " through DevTools...")

        ids := GetStoryIDsFromDevTools(pageURL)

        if (ids.Length = 0) {
            ToolTip()
            MsgBox(
                "No story IDs were extracted from page " pageNumber "."
                . "`n`nCheck that the Fimfiction list is accessible and"
                . " that the DevTools Console accepted the JavaScript."
            )
            break
        }

        newIDs := []

        for id in ids {
            if !seen.Has(id) {
                seen[id] := true
                newIDs.Push(id)
            }
        }

        if (newIDs.Length = 0)
            break

        for id in newIDs {
            ToolTip(
                "Downloading story " id
                . "`nPage: " pageNumber
                . "`nCompleted: " downloaded
            )

            if DownloadStory(id)
                downloaded++
            else
                failed++
        }

        if !allPages
            break

        pageNumber++
    }

    ToolTip()

    MsgBox(
        "Finished processing the story list."
        . "`n`nDownloaded: " downloaded
        . "`nFailed or timed out: " failed
        . "`n`nOutput folder:`n" outputDir,
        "Fimfiction Downloader"
    )
}

ParseParameters(text) {
    result := Map()

    ; Extract options, supporting quoted values and URLs.
    if RegExMatch(text, '(?i)(?:^|\s)(?:-o|--out)\s+(?:"([^"]+)"|(\S+))', &m)
        result["out"] := (m[1] != "") ? m[1] : m[2]

    if RegExMatch(text, '(?i)(?:^|\s)(?:-a|--adult)\s+(\S+)', &m)
        result["adult"] := m[1]

    if RegExMatch(text, '(?i)(?:^|\s)(?:-f|--format)\s+(\S+)', &m)
        result["format"] := m[1]

    if RegExMatch(text, '(?i)(?:^|\s)(?:-r|--range)\s+(\S+)', &m)
        result["range"] := m[1]

    ; Find the first HTTP(S) URL, allowing optional surrounding quotes.
    if RegExMatch(text, 'i)(https?://[^\s""]+)', &m)
        result["url"] := RTrim(m[1], ".,;")

    return result
}


GetStoryIDsFromDevTools(url) {
    global browserHwnd, browserExe

    WinActivate("ahk_id " browserHwnd)
    Sleep(300)

    Send("^l")
    Sleep(150)
    SendText(url)
    Send("{Enter}")
    Sleep(3000)

    savedClip := ClipboardAll()
    A_Clipboard := ""

    if (browserExe = "firefox.exe")
        Send("^+k")
    else
        Send("^+j")

    Sleep(1500)

    js := "copy(Array.from(document.querySelectorAll('a.story_link'))"
        . ".map(a => {let m = a.href.match(/fimfiction\.net\/story\/(\d+)/);"
        . "return m ? m[1] : '';})"
        . ".filter(Boolean).filter((id,i,arr) => arr.indexOf(id) === i).join(','))"

    SendText(js)
    Sleep(200)
    Send("{Enter}")
    Sleep(500)

    idsText := A_Clipboard

    if (idsText = "") {
        A_Clipboard := savedClip
        if (browserExe = "firefox.exe")
            Send("^+k")
        else
            Send("^+j")
        return []
    }

    if (browserExe = "firefox.exe")
        Send("^+k")
    else
        Send("^+j")

    Sleep(300)
    A_Clipboard := savedClip

    ids := []
    for id in StrSplit(Trim(idsText), ",") {
        id := Trim(id)
        if RegExMatch(id, "^\d+$")
            ids.Push(id)
    }

    return ids
}


DownloadStory(id) {
    global browserHwnd, browserExe, fileFormat, outputDir, downloadDir

    before := SnapshotFiles(downloadDir)
    downloadURL := "https://www.fimfiction.net/story/download/" . id . "/" . fileFormat

    WinActivate("ahk_id " browserHwnd)
    Sleep(200)
    Send("^l")
    Sleep(100)
    SendText(downloadURL)
    Send("{Enter}")

    ; Wait up to 10 seconds for a native Save As dialog.
    dialogHwnd := 0
    startTime := A_TickCount

    while (A_TickCount - startTime < 10000) {
        ; Common native Windows file-dialog class.
        if WinExist("ahk_class #32770") {
            candidateHwnd := WinExist("ahk_class #32770")
            candidateTitle := WinGetTitle("ahk_id " candidateHwnd)

            ; Avoid interacting with unrelated dialogs.
            if InStr(candidateTitle, "Save")
                || InStr(candidateTitle, "Download")
                || InStr(candidateTitle, "As") {
                dialogHwnd := candidateHwnd
                break
            }
        }

        Sleep(250)
    }

    if (dialogHwnd) {
        WinActivate("ahk_id " dialogHwnd)

        target := UniqueDestination(outputDir, id "." fileFormat)

        ; Standard Save As dialogs accept a full path in the filename field.
        Sleep(300)
        Send("^a")
        SendText(target)
        Sleep(200)
        Send("{Enter}")

        ; Wait for the dialog to close.
        if WinWaitClose("ahk_id " dialogHwnd,, 15) {
            return WaitForDestination(target, 120)
        }

        ; The dialog may still be open because a confirmation is required.
        ; Press Enter once more only while the same dialog remains active.
        if WinExist("ahk_id " dialogHwnd) {
            WinActivate("ahk_id " dialogHwnd)
            Sleep(300)
            Send("{Enter}")

            if WinWaitClose("ahk_id " dialogHwnd,, 10)
                return WaitForDestination(target, 120)
        }

        return false
    }

    ; No native Save As dialog: wait for an automatic browser download.
    candidate := WaitForNewDownload(before, 120)

    if (candidate = "")
        return false

    target := UniqueDestination(outputDir, candidate.name)

    try {
        FileMove(candidate.path, target)
        return true
    } catch {
        return false
    }
}

SnapshotFiles(folder) {
    files := Map()
    Loop Files folder "\*", "F" {
        files[A_LoopFileFullPath] := A_LoopFileSize
    }
    return files
}

WaitForNewDownload(before, timeoutSeconds) {
    global downloadDir

    start := A_TickCount
    lastPath := ""
    lastSize := -1
    stable := 0

    while ((A_TickCount - start) < timeoutSeconds * 1000) {
        Sleep 500

        found := ""
        Loop Files downloadDir "\*", "F" {
            name := A_LoopFileName
            path := A_LoopFileFullPath

            if RegExMatch(name, "i)\.(part|crdownload|tmp)$")
                continue

            if !before.Has(path) {
                found := path
                break
            }
        }

        if (found = "")
            continue

        size := FileGetSize(found)
        if (found = lastPath && size = lastSize)
            stable++
        else
            stable := 0

        lastPath := found
        lastSize := size

        ; Require several consecutive stable-size checks.
        if (stable >= 4) {
            SplitPath found, &name
            return {path: found, name: name}
        }
    }

    return ""
}

WaitForDestination(path, timeoutSeconds) {
    start := A_TickCount
    while ((A_TickCount - start) < timeoutSeconds * 1000) {
        if FileExist(path)
            return true
        Sleep 500
    }
    return false
}

UniqueDestination(folder, filename) {
    path := folder "\" filename
    if !FileExist(path)
        return path

    SplitPath filename, , , &ext, &nameNoExt
    n := 1
    loop {
        candidate := folder "\" nameNoExt "_" n "." ext
        if !FileExist(candidate)
            return candidate
        n++
    }
}

GetPageNumber(url) {
    if RegExMatch(url, "i)[?&]page=(\d+)", &m)
        return Integer(m[1])
    return 1
}

AddQuery(url, key, value) {
    if RegExMatch(url, "i)([?&])" key "=")
        return RegExReplace(url, "i)([?&])" key "=[^&]*", "$1" key "=" value)

    sep := InStr(url, "?") ? "&" : "?"
    return url sep key "=" value
}

SetPageNumber(url, page) {
    if RegExMatch(url, "i)[?&]page=")
        return RegExReplace(url, "i)([?&])page=\d+", "$1page=" page)

    sep := InStr(url, "?") ? "&" : "?"
    return url sep "page=" page
}

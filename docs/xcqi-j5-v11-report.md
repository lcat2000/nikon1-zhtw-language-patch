# J5 patched v11 on a Japanese-market body — test report

English | [繁體中文](#繁體中文)

For **XCQi**, author of [Nikon-1-custom-firmware](https://github.com/XCQi/Nikon-1-custom-firmware).

Hi XCQi, thank you for the J5 custom firmware. I tested the v11 language-menu unlock on a Japanese-market J5 (C1.01).

**Summary:** with v11's cleared language-item flags plus three small changes, the language menu works on a Japanese-market body. All 32 languages are listed with correct names, Traditional Chinese is kept after power-off, and Japanese remains available.

All addresses below are runtime addresses (image offset + `0x80000`), in your v11 release file `J5_0101_patched_v11.bin` (SHA-256 `2232768f…8765fdf`).

## Findings

### 1. The language screen still takes its Japan path

The language screen reads property 1 (region) at `0x424B90` (init) and `0x424E00` (key handler). With region 0 it builds the 2-entry Japan list (table at `0x01599CA0`, count 2) instead of the 32-entry list at `0x01599CB0`.

I did not flash plain v11. But earlier, on v10, forcing only the screen path (masks still set) showed two rows labelled Български and Čeština. So the number of rows (from the item masks) and the screen's own list are independent, and both must be switched.

**Change:** both `bl 0x3C5554` → `movs r0,#1; str r0,[r3]` (bytes `01 20 18 60`).

### 2. Three language names lacked glyphs

With change 1 on v11, all 32 items appear and work, but हिन्दी, عربي and فارسی were drawn with missing glyphs (Hindi lost its न्द conjunct; Arabic and Persian were boxes).

The list draws each name after the temporary language switch at `0x168452`. Its font getter goes through the veneer at `0x2F6094` to font set B (`0x5AF1B0`, descriptors at `0x144DE38 + 0x90`), whose Arabic and Hindi fonts are reduced subsets. `setLanguage` (`0x1684A0`) uses set A through `0x2F609C`.

**Change:** literal at `0x2F6098`, `0x005AF1B1` → `0x005AF199`. The veneer has no other callers (three calls, all in `0x168452`). All names then render correctly, and Arabic and Persian are right-aligned.

### 3. The masks also control which saved languages persist

On v10 (flags still set), selecting a non-Japanese value took effect immediately but reverted to Japanese after power-off. With v11's cleared flags, Traditional Chinese is retained. So the masks appear to gate which saved values are valid, not only which rows are visible.

## Patch

| Change | Runtime address | Bytes |
|---|---|---|
| Language screen init, region read | `0x00424B90` | `a0 f7 e0 fc` → `01 20 18 60` |
| Language screen key handler, region read | `0x00424E00` | `a0 f7 a8 fb` → `01 20 18 60` |
| Temporary-switch font getter veneer, set B → set A | `0x002F6098` | `b1 f1 5a 00` → `99 f1 5a 00` |
| Embedded CRC | package `0x175A6E0` | recomputed |

`patch_j5.py` in this repository applies exactly these changes to your v11 release file, verified by SHA-256. No firmware is redistributed. Output SHA-256: `974a1d37ce577c862021f042c1bd7cd58ebafc53c17c79837f7471bf6653ac95`.

Tested on one Japanese-market J5 only; only the language menu and Traditional Chinese were checked. Feel free to fold any of this into your release.

— Kai Chang ([lcat2000](https://github.com/lcat2000))

---

## 繁體中文

給 [Nikon-1-custom-firmware](https://github.com/XCQi/Nikon-1-custom-firmware) 的作者 **XCQi**。

XCQi 您好，感謝您的 J5 自製韌體。我在一台日本版 J5（C1.01）上測試了 v11 的語言選單解鎖。

**摘要：** 在 v11 已清除語言項目旗標的基礎上，再加三處小修改，日本版機身的語言選單就能正常運作：32 種語言全部列出、名稱正確顯示，繁體中文關機後會保留，日文也照樣可以選。

以下位址都是執行位址（映像檔位移 + `0x80000`），對應您的 v11 發行檔 `J5_0101_patched_v11.bin`（SHA-256 `2232768f…8765fdf`）。

### 1. 語言畫面仍走日本機流程

語言畫面在 `0x424B90`（初始化）和 `0x424E00`（按鍵處理）讀取屬性 1（地區）。地區為 0 時，會用兩項的日本清單（表格在 `0x01599CA0`，數量 2），而不是 `0x01599CB0` 的 32 項清單。

我沒有刷過 v11 原版。但先前在 v10 上，只強制改語言畫面（遮罩仍有效）時，畫面出現兩列，顯示 Български 和 Čeština。可見列數（由項目遮罩決定）和語言畫面自己的清單是各自獨立的，兩者都要切換。

**修改：** 兩處 `bl 0x3C5554` → `movs r0,#1; str r0,[r3]`（bytes `01 20 18 60`）。

### 2. 三個語言名稱缺字形

在 v11 上加入第 1 項修改後，32 個項目都會出現並能正常使用，但 हिन्दी、عربي、فارسی 這三個名稱缺字形（印地文缺 न्द 連寫字，阿拉伯文和波斯文顯示成方塊）。

清單畫每個名稱前，會在 `0x168452` 暫時切換到該語言。這個函式取得字型時，經由 `0x2F6094` 的跳轉取得第二組字型（`0x5AF1B0`，描述表在 `0x144DE38 + 0x90`），其中的阿拉伯文和印地文字型是精簡子集。`setLanguage`（`0x1684A0`）則經由 `0x2F609C` 使用第一組。

**修改：** `0x2F6098` 的位址常數 `0x005AF1B1` → `0x005AF199`。這個跳轉沒有其他呼叫者（共 3 處，都在 `0x168452` 裡）。修改後所有名稱都正確顯示，阿拉伯文和波斯文靠右對齊。

### 3. 遮罩也決定哪些已存的語言會被保留

在 v10 上（旗標仍在），選非日文的設定值會立即生效，但關機後會回到日文。v11 清除旗標後，繁體中文會被保留。可見遮罩不只決定哪些列可見，也決定哪些已存的設定值有效。

### 修改內容

| 修改 | 執行位址 | Bytes |
|---|---|---|
| 語言畫面初始化，地區讀取 | `0x00424B90` | `a0 f7 e0 fc` → `01 20 18 60` |
| 語言畫面按鍵處理，地區讀取 | `0x00424E00` | `a0 f7 a8 fb` → `01 20 18 60` |
| 暫時切換語言的字型取得跳轉，第二組 → 第一組 | `0x002F6098` | `b1 f1 5a 00` → `99 f1 5a 00` |
| 內嵌 CRC | 封裝位移 `0x175A6E0` | 重新計算 |

本儲存庫的 `patch_j5.py` 只會對您的 v11 發行檔套用上述修改，並以 SHA-256 核對，不散布任何韌體。輸出 SHA-256：`974a1d37ce577c862021f042c1bd7cd58ebafc53c17c79837f7471bf6653ac95`。

只在一台日本版 J5 上測試過，實機只檢查了語言選單與繁體中文。歡迎將任何內容納入您的發行版本。

— Kai Chang（[lcat2000](https://github.com/lcat2000)）

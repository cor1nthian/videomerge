# videomerge
Video merge script creating a video file from a bunch if video files and (optionally) timestamp text data list.

Script uses fffmpeg / ffprobe exe tools, read more on this in script comments

Tested with Windows 10

Can be called with arguments:
| Position | Suggested type | Description |
| --- | --- | --- |
| 1 | String | Path to folder containing video files and image
| 2 | Bool | If true, creates exact chapter marks (adds half a second to every chapter start mark, which is enough even in case of not exact K-Lite player rewind)
| 3 | Bool | If true, creates twxt file containg chapter info

Script return codes:
| Code | Description |
| --- | --- |
| 0 | Successful execution |
| 1 | Content folder does not exist |
| 2 | Content folder path not found |
| 3 | Exact chapter timestaamp mark variable not set |
| 4 | Text chapter creation mark variable not set |
| 5 | No files found in specified (content) folder |
| 6 | Could not create video file list |
| 7 | Could not get media duration |

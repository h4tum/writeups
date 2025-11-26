# Writeup: To Shreds You Say (WHY2025 CTF)

**Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
**Challenge:** To Shreds You Say
**Category:** Forensics
**Solved by:** [dopri](https://github.com/DoPri/)

We are provided with a PDF file `ToShredsYouSay-1.pdf`.

## Initial Analysis

The challenge title "To Shreds You Say" hints at reconstructing a shredded document. Opening the PDF reveals it contains a scan of shredded paper strips containing frames.

## Solution

I extracted the strips from the PDF and reassembled them. By reordering the strips in the correct order, the original document was reconstructed, revealing the flag. I used [photopea](https://www.photopea.com/) to manually arrange the strips.

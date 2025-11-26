# Writeup: Bitlocked (WHY2025 CTF)

- **Event:** [WHY2025 CTF](https://ctf.why2025.org/) ([CTFTime](https://ctftime.org/event/2680))
- **Challenge:** Bitlocked
- **Category:** Forensics
- **Solved by:** [dopri](https://github.com/DoPri/)

We are provided with a 7-zip archive `SD_card.7z` (containing a disk image) and a photo `Photo_SD_card.jpg`.

## Initial Analysis

I started by extracting `SD_card.7z` to get the disk image `SD_card.img`.
I also examined `Photo_SD_card.jpg`, which showed a picture of the BitLocker Recovery Key partially obscured by an SD card.

I wrote a script designed to brute-force the missing digits of the recovery key.

## Solution

### Step 1: Recovering the Key

The key visible in the photo was incomplete. I used [crunch](https://www.kali.org/tools/crunch/) to generate a wordlist and [bitcracker](https://github.com/e-ago/bitcracker) to brute-force the missing characters. After running the script, I obtained the full recovery key: `718894-682847-228371-253055-328559-381458-030668-047839`.

### Step 2: Decrypting the Image

With the full recovery key in hand, I used `dislocker` to decrypt and mount the image on my Linux system:

```bash
mkdir -p /mnt/bitlocker

dislocker -f SD_card.img -p718894-682847-228371-253055-328559-381458-030668-047839 -- /mnt/bitlocker

mkdir -p /mnt/data
mount /mnt/bitlocker/dislocker-file /mnt/data
```

Once mounted, I browsed `/mnt/data` to find the flag.

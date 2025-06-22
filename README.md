# Dictionary-Based-Password-Cracker

This tool is designed to crack password hashes using a dictionary attack. It supports common hash types (MD5, SHA-1, SHA-256, SHA-512) and allows users to apply case variations to increase the chances of a successful match.

### Requirements
- Python 3.8 or newer
- tqdm package installed (used for progress display)

To install `tqdm`, run:
```bash
`pip install tqdm`
```
---

### How to Use

#### Step 1: Prepare Input Files
You will need:
- A hash list file (`.txt`) with one hash per line
  - Note that in this repo there are 12 hash list files provided for testing, they are listed in a comment at the top of `main.py`. Feel free to use these for your testing.
- A dictionary file (`.txt`) with one word per line (e.g. `rockyou.txt`)

#### Step 2: Run the Program
From a terminal or command prompt, navigate to the folder containing the script and run:
```bash
python main.py
```

#### Step 3: Follow the Prompts
The program will ask you for:
1. The path to your hash file
    - Example: `C:\Users\YourName\Documents\hashes.txt`
2. The path to your dictionary file
    - Example: `C:\Users\YourName\Documents\rockyou.txt`
3. Whether to check **UPPERCASE** versions of each dictionary word (`y` or `n`)
4. Whether to check **lowercase** versions (`y` or `n`)
5. Whether to check **TitleCase** versions (`y` or `n`)

Once options are selected, the cracking process begins. A progress bar will display progress in real time.

---

### Output
The program outputs results to a file called: `cracked_hashes.csv`

Each line in the file contains: `<original_hash>,<matching_password>`
- For example: `5f4dcc3b5aa765d61d8327deb882cf99,password`

The CSV file will be updated each time the program finds a match, and results are appended, not overwritten.

### Notes and Tips
- The program identifies hash types automatically based on length
- Dictionary files must be in plain text and encoded in a compatible format (the script reads using `"latin-1"` to support extended characters)
- If a file path is incorrect or cannot be read, you will be prompted to re-enter it
- If a hash does not match any dictionary entry, it will be skipped, and you will be notified in the terminal output

### Example Session

```pgsql
Please enter the hashes file path: hashes.txt 
The file path 'hashes.txt' is valid. 
The file extension is: .txt  

Please enter the dictionary file path: rockyou.txt 
The file path 'rockyou.txt' is valid. 
The file extension is: .txt  

Check UPPERCASE versions? (y/n): y 
Check lowercase versions? (y/n): y 
Check TitleCase versions? (y/n): n  

Cracking hashes: 100%|████████████████████████████████████████| 5/5 [00:01<00:00,  4.91it/s]  
Match found: password 

No match found. 

Match found: 123456

Cracked Hashes: 3 
Cracked Hash File: cracked_hashes.csv
```

## Algorithm

Final version of the hash cracking algorithm...

```mermaid
---
config:
  theme: redux
  layout: dagre
---
flowchart TD
    A(["Program Starts"]) --> n1["Prompt for input file"]
    n1 --> n3["Is file type / content is valid"]
    n3 --> n5["True"] & n7["False"]
    n7 --> n1
    n5 --> n8["Prompt for wordlist"]
    n8 --> n9["Is file type / content is valid &amp; accessible"]
    n9 --> n11["True"] & n12["False"]
    n12 --> n8
    n11 --> n18["Prompt for dictionary type variations"]
    n6["Convert hashes in input file into list strings"] --> n25["Loop through list items"]
    n13["Check hash legth"] -- 32 Characters --> n14["MD5"]
    n13 -- 40 Characters --> n15["SHA1"]
    n13 -- 128 Characters --> n17["SHA512"]
    n13 -- 64 Characters --> n16["SHA256"]
    n18 --> n19["If variation is specified"]
    n19 -- Uppercase --> n20@{ label: "<span style=\"background-color:\">Uppercase = True</span>" }
    n19 -- Lowercase --> n21["Lowercase = True"]
    n19 -- Titlecase --> n22["Titlecase = True"]
    n20 --> n6
    n21 --> n6
    n22 --> n6
    n14 --> n23["Initiate <b>for</b> loop, for items in list"]
    n15 --> n23
    n17 --> n23
    n16 --> n23
    n23 --> n49["Initiate progress bar - updates for each iteration"]
    n23 -- Loop exited --> n44["Stop"]
    n25 --> n13
    n26["Hash next string in dictionary list"] --> n27["Compare dictionary hash to input hash from user"]
    n27 --> n28["Check for match"]
    n28 --> n29["True"] & n30["False"]
    n30 --> n32["Check variation variables<br>(First True statement runs)"]
    n29 --> n31["Add hash and plaintext string to CSV file"]
    n32 --> n33["If Uppercase = True"] & n34["If Lowercase = True"] & n35["If Titlecase = True"] & n37["Else"]
    n33 -- ".upper()" --> n36["Set variation variables to false"]
    n37 --> n26
    n34 -- ".lower()" --> n36
    n35 -- ".title()" --> n36
    n36 --> n38["Apply method to string"]
    n31 --> n26
    n38 --> n40["Hash new dictionary string"]
    n40 --> n27
    n44 --> n45["Display number of cracked hashes and display CSV file path"]
    n45 --> n47["Program Ends"]
    n49 --> n26
    n1@{ shape: lean-r}
    n3@{ shape: diam}
    n8@{ shape: lean-r}
    n9@{ shape: diam}
    n12@{ shape: rect}
    n18@{ shape: lean-r}
    n6@{ shape: rect}
    n13@{ shape: diam}
    n19@{ shape: diam}
    n20@{ shape: rect}
    n44@{ shape: stop}
    n28@{ shape: diam}
    n32@{ shape: diam}
    n47@{ shape: rounded}
    style A fill:#00C853
    style n47 fill:#D50000
```

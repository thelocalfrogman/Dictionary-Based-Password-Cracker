# Dictionary-Based-Password-Cracker

Current version (pre-code) hash cracking algorithm
Can also be found on Mermaid [here](https://www.mermaidchart.com/app/projects/55559564-4b3b-4298-a2aa-04db4e233f2b/diagrams/0b39b44d-468d-4ed4-852f-a402242a71af/version/v0.1/edit).

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

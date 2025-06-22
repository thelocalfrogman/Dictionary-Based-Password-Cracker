// Authors: George Ferres, William Chaston
// We simplified some sections but core functionality is the same

// Import required standard libraries - or their equivelants
IMPORT os
IMPORT csv
IMPORT hashlib
IMPORT tqdm FROM tqdm
IMPORT Path FROM pathlib

// Declare global variables with default placeholder values
SET file_path TO "a"
SET dic_path  TO "a"
SET hash_count TO 0

// Prompt user for the hashes file path and validate it
FUNCTION whathash()
    PROMPT "Please enter the hashes file path: " AND STORE INPUT IN file_path
    IF Path(file_path) EXISTS THEN
        DISPLAY "The file path '" + file_path + "' is valid."
        SET file_name TO file_path
        SET file_extension TO Path(file_name).suffix
        DISPLAY "The file extension is: " + file_extension
        RETURN file_path
    ELSE
        DISPLAY "The file path '" + file_path + "' does not exist. Please check and try again."
        RETURN CALL whathash()
    END IF
END FUNCTION

// Prompt user for the dictionary file path and validate it
FUNCTION whatdic()
    PROMPT "Please enter the dictionary file path: " AND STORE INPUT IN dic_path
    IF Path(dic_path) EXISTS THEN
        DISPLAY "The file path '" + dic_path + "' is valid."
        SET file_name TO dic_path
        SET file_extension TO Path(file_name).suffix
        DISPLAY "The file extension is: " + file_extension
        RETURN dic_path
    ELSE
        DISPLAY "The file path '" + dic_path + "' does not exist. Please check and try again."
        RETURN CALL whatdic()
    END IF
END FUNCTION

// Determine suitable hash algorithm based on hash string length
FUNCTION detect_hash_type(hash_string)
    SET length TO LENGTH(hash_string)
    IF length == 32 THEN
        RETURN hashlib.md5
    ELIF length == 40 THEN
        RETURN hashlib.sha1
    ELIF length == 64 THEN
        RETURN hashlib.sha256
    ELIF length == 128 THEN
        RETURN hashlib.sha512
    ELSE
        RETURN null
    END IF
END FUNCTION

// Attempt case variation matches for a single dictionary word against target hash
FUNCTION try_variations(word, target_hash, hash_func, use_upper, use_lower, use_title)
    INITIALISE attempts AS LIST OF (word, "original")
    IF use_upper IS TRUE THEN
        APPEND (UPPER(word), "upper") TO attempts
    END IF
    IF use_lower IS TRUE THEN
        APPEND (LOWER(word), "lower") TO attempts
    END IF
    IF use_title IS TRUE THEN
        APPEND (TITLE(word), "title") TO attempts
    END IF

    FOR EACH (variant, label) IN attempts DO
        SET word_hash TO hash_func(ENCODE(variant)).hexdigest()
        IF word_hash == target_hash THEN
            RETURN variant
        END IF
    END FOR
    RETURN null
END FUNCTION

// Compare each input hash against the dictionary to find matching word
FUNCTION check_hashes(input_list, hash_count)
    FOR EACH target_hash IN tqdm(input_list, desc="Cracking hashes") DO
        DISPLAY "Checking hash: " + target_hash
        SET hash_func TO CALL detect_hash_type(target_hash)
        IF hash_func IS null THEN
            DISPLAY "Unknown hash type"
            CONTINUE LOOP
        END IF

        SET use_upper TO use_upper_input
        SET use_lower TO use_lower_input
        SET use_title TO use_title_input
        
        SET found TO FALSE

        OPEN dic_path AS wordlist_file
            FOR EACH line IN wordlist_file DO
                SET word TO STRIP(line)
                SET match TO CALL try_variations(word, target_hash, hash_func, use_upper, use_lower use_title)
                
                IF match IS NOT null THEN
                    DISPLAY "Match found: " + match
                    ADD 1 TO hash_count
                    OPEN "cracked_hashes.csv" IN append MODE AS csvfile
                        WRITE ROW [target_hash, match] TO csvfile
                        CLOSE csvfile
                SET found TO TRUE
                BREAK
                END IF
            END FOR
        CLOSE wordlist_file

        IF found IS FALSE THEN
            DISPLAY "No match found."
        END IF
    END FOR
    RETURN hash_count
END FUNCTION

// Program execution
SET file_path TO CALL whathash()
SET dic_path TO CALL whatdic()

// Request variation options from user
PROMPT "Check UPPERCASE versions? (y/n): " AND LOWER AND STORE BOOLEAN RESULT IN use_upper_input
PROMPT "Check lowercase versions? (y/n): " AND LOWER AND STORE BOOLEAN RESULT IN use_lower_input
PROMPT "Check TitleCase versions? (y/n): " AND LOWER AND STORE BOOLEAN RESULT IN use_title_input

OPEN file_path AS input_file
    SET input_list TO LIST OF STRIP(line) FOR EACH line IN input_file

SET hash_count TO CALL check_hashes(input_list, hash_count)
DISPLAY "Cracked Hashes: " + hash_count
DISPLAY "Cracked Hash File: cracked_hashes.csv"
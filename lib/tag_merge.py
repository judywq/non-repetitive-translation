import json


def view_word_list(word_list):
    for word in word_list:
        print(f"Surface: {word.surface}, ID: {word.id}, Ref: {word.ref}")
    print('-' * 20)
    
def find_non_negative_consecutive_sequences(lst):
    # Initialize an empty dictionary to store the sequences and their indices
    sequences_dict = {}

    # Iterate over the list with an index
    for i in range(len(lst) - 1):
        # Skip if the current element is negative
        if lst[i] < 0:
            continue
        
        # Start a potential sequence
        seq = [lst[i]]
        # Iterate through the remaining elements to build the sequence
        for j in range(i + 1, len(lst)):
            # Check if the next number is non-negative
            if lst[j] >= 0:
                seq.append(lst[j])
                # Convert the sequence list to a tuple to use it as a dictionary key
                seq_tuple = tuple(seq)
                # Initialize the key in the dictionary if it doesn't exist
                if seq_tuple not in sequences_dict:
                    sequences_dict[seq_tuple] = []
                # Append the starting index of the sequence to the dictionary
                sequences_dict[seq_tuple].append(i)
            else:
                # Stop if the next number is negative
                break

    # Filter out sequences that occur only once
    filtered_sequences = {seq: indices for seq, indices in sequences_dict.items() if len(indices) > 1}

    return filtered_sequences

def merge_word_sequences(word_list):
    # Extract word IDs from the word_list
    word_ids = [w.id for w in word_list]
    
    # Find sequences of non-negative IDs that occur more than once
    sequences_dict = find_non_negative_consecutive_sequences(word_ids)
    
    # Create a new dictionary to store the new IDs for each sequence
    new_id_dict = {}
    # HACK: Set the starting ID for the new sequences to avoid conflicts with old ones
    next_new_id = 1000
    
    # Assign new IDs to the sequences
    for seq in sequences_dict:
        new_id_dict[seq] = next_new_id
        next_new_id += 1

    # Update word_list with merged sequences
    for seq, indices in sequences_dict.items():
        for index in indices:
            # Set the same new ID and ref for all words in the sequence
            for offset in range(len(seq)):
                if offset == 0:
                    if word_list[index + offset].id < 0:
                        # Skip if the ID is negative, meaning it's already been merged
                        break
                    word_list[index + offset].id = new_id_dict[seq]
                    word_list[index + offset].surface = "".join(w.surface for w in word_list[index:index + len(seq)])
                else:
                    word_list[index + offset].clear()
            # view_word_list(word_list)
            
    word_list = update_word_id_and_ref(word_list)
    
    return word_list            

def update_word_id_and_ref(word_list):
    # Update the ids, since there may be gaps in the sequence
    next_new_id = 0
    id_map = {}
    for word in word_list:
        if word.id >= 0 and word.id not in id_map:
            id_map[word.id] = next_new_id
            next_new_id += 1
    for word in word_list:
        if word.id >= 0:
            word.id = id_map[word.id]                
            
    # Update the ref numbers for the merged sequences
    new_ref_dict = {}
    for word in word_list:
        if word.id >= 0:
            if word.id not in new_ref_dict:
                new_ref_dict[word.id] = 0
            word.ref = new_ref_dict[word.id]
            new_ref_dict[word.id] += 1

    return word_list


def merge_proof_reading_result(raw_translation, proof_reading):
    raw_translation_dict = json.loads(raw_translation)
    proof_reading_dict = json.loads(proof_reading)

    final_translation = {**raw_translation_dict}
    
    if proof_reading_dict["changed"].lower() == "yes":
        final_translation["en_translation"] = proof_reading_dict["en_translation_updated"]
        final_translation["targets"] = proof_reading_dict["targets_updated"]    
    return final_translation

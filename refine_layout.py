
import re
import os

def refine_layout_file(file_path):
    print(f"Refining layout for {file_path}")
    with open(file_path, "r") as f:
        lines = f.readlines()
        
    new_lines = []
    seen_portraits = set()
    
    # Regex for Manual Figure Captions
    # Matches: \textit{Figure X: ...}
    # We want to remove these entire lines.
    caption_pattern = re.compile(r'^\s*\\textit\{Figure\s*\d+:.*\}')
    
    # Regex for Portrait Margin Notes
    # Matches: \automarginnote{\includegraphics[...]{Portraits/Chapter-Introduction/Name.jpg}}
    # We want to extract the filename "Name.jpg" and check if it's seen.
    portrait_pattern = re.compile(r'\\automarginnote\{.*\\includegraphics\[.*\]\{Portraits/.*?/([^/]+\.(?:jpg|png))\}.*\}')
    
    
    # 1. First Pass: Analyze Density and Find Candidate Slots
    # We want to find every mention of every person to know where we CAN place their portrait.
    # People: Arthur Samuel, Tom Mitchell, Geoffrey Hinton, Yann LeCun, Yoshua Bengio, Frank Rosenblatt, Alan Turing, Donald Hebb
    # (We can extract these names from the file itself or hardcode common ones)
    
    # Actually, simpler approach for "Smart Placement":
    # 1. Collect all `\automarginnote` commands.
    # 2. Collect all locations (line numbers) where the person's name appears.
    # 3. Re-distribute the margin notes.
    
    # BUT, that changes the file structure significantly.
    # Let's try a "Push Down" strategy.
    # If we find a margin note for Person X on Line L, and there are already N margin notes in the last K lines...
    # ... we REMOVE it from Line L and try to re-insert it at the NEXT mention of Person X.
    
    # Step 1: Clean Up First (Captions & Widths) & Map Content
    clean_lines = []
    
    # Aggressive Caption Regex: Matches "\textit{Figure" and seems to end with "}"
    # Also catch cases where it's at the end of a line or within text? 
    # User said "line 75": \textit{Figure 3: ...}
    caption_pattern = re.compile(r'\\textit\{Figure\s*\d+:[^}]*\}')
    
    # Portrait Pattern
    # Portrait Pattern (Handle nested braces for includegraphics)
    # Matches: \automarginnote{\includegraphics[...]{...}}
    # We explicitly look for the inner {} of includegraphics to ensure we capture the outer }
    portrait_pattern_extract = re.compile(r'(\\automarginnote\{.*?\\includegraphics\[[^\]]*\]\{Portraits/.*?/([^/]+\.(?:jpg|png))\}.*?\})')
    
    # Figure Width Pattern
    # \includegraphics[width=0.9\linewidth] -> 1.0
    width_pattern = re.compile(r'width=0\.9\\linewidth')
    
    person_locations = {} # { "ArthurSamuel.jpg": [line_idx1, line_idx2, ...] }
    
    # Pre-scan for Names (Approximation based on filename)
    # ArthurSamuel.jpg -> "Arthur Samuel" or "Samuel"
    # We need a mapping or just fuzzy string match.
    
    # Let's do a single pass to Clean and separate Portraits.
    
    content_lines_without_portraits = []
    extracted_portraits = [] # (original_line_idx, portrait_filename, full_command_string)
    
    for i, line in enumerate(lines):
        # Fix Width
        line = width_pattern.sub(r'width=1.0\\linewidth', line)
        
        # Remove Captions (Replace with empty string)
        if caption_pattern.search(line):
             print(f" - Removing caption on line {i+1}")
             line = caption_pattern.sub('', line)
             
        # Extract Portraits
        matches = list(portrait_pattern_extract.finditer(line))
        # Remove them from the line for now, we will re-inject them smartly.
        curr_line_portraits = []
        for match in reversed(matches):
            full_cmd = match.group(1)
            filename = match.group(2)
            extracted_portraits.append({'filename': filename, 'cmd': full_cmd, 'original_line': i})
            
            start, end = match.span()
            line = line[:start] + line[end:]
            
        content_lines_without_portraits.append(line)

    # Step 2: Build Person Location Map
    # Map "ArthurSamuel.jpg" -> "Arthur Samuel" (Split CamelCase or use heuristic)
    def filename_to_name(fname):
        name = fname.replace(".jpg", "").replace(".png", "")
        # "ArthurSamuel" -> "Arthur Samuel"
        # Simple regex to split CamelCase
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', name)

    for p in extracted_portraits:
        fname = p['filename']
        name = filename_to_name(fname)
        
        # Find all mentions in cleaned text
        mentions = []
        for idx, txt in enumerate(content_lines_without_portraits):
            if name in txt: # exact substring match
                mentions.append(idx)
        
        p['mentions'] = mentions
        
    # Step 3: Distribute
    # Rule: Minimum 100 lines between margin notes? Or just spread them out?
    # We have 18 pages (~800 lines?). 17 portraits.
    # Ideally 1 portrait every 40-50 lines.
    
    # Sort portraits by their FIRST appearance in original text (priority)
    # actually, we want to place them near mentions.
    
    # Step 3: Distribute - "Must-Place Best-Fit" Strategy
    # We MUST place every unique file exactly once.
    # We want to pick the mention that maximizes distance from other placed portraits.
    
    final_placements = {} # line_idx -> list of commands
    placed_lines = []     # List of line numbers where we dropped a portrait
    
    # Unique set of filenames to place
    unique_files = list(set([p['filename'] for p in extracted_portraits]))
    
    # Map filename -> full latex command
    file_to_cmd = {p['filename']: p['cmd'] for p in extracted_portraits}
    
    # Sort people by their FIRST mention line (to keep some chronological order)
    # or process them in order of "scarcity" (fewest mentions first)?
    # Let's stick to First Mention order to respect the flow, but allow them to slide down.
    
    people_order = [] 
    for fname in unique_files:
        if not fname: continue
            
        # Find all mentions
        my_mentions = []
        name = filename_to_name(fname)
        
        # 1. Exact Name Matches
        for idx, txt in enumerate(content_lines_without_portraits):
            if name in txt:
                my_mentions.append(idx)
        
        # 2. If no text mentions (fallback), use the original line it was found on
        if not my_mentions:
            # Find original line from extraction
            for p in extracted_portraits:
                if p['filename'] == fname:
                    my_mentions.append(p['original_line'])
                    break
        
        # Deduplicate and sort mentions
        my_mentions = sorted(list(set(my_mentions)))
        
        if not my_mentions:
            print(f"!! WARNING: Could not find any placement slot for {fname}")
            continue
            
        people_order.append({
            'filename': fname,
            'mentions': my_mentions,
            'first_mention': my_mentions[0],
            'cmd': file_to_cmd[fname]
        })
        
    # Sort by first mention
    people_order.sort(key=lambda x: x['first_mention'])
    
    for person in people_order:
        fname = person['filename']
        mentions = person['mentions']
        
        best_line = -1
        max_min_dist = -1
        
        # Evaluate each mention slot
        # We want the slot that is furthest from any existing placed line
        
        candidates = []
        
        for m_line in mentions:
            # Calculate distance to nearest neighbour
            if not placed_lines:
                dist = 1000 # Infinity equivalent
            else:
                dist = min([abs(m_line - pl) for pl in placed_lines])
            
            candidates.append((dist, m_line))
            
        # Sort candidates by distance (descending) -> maximize spacing
        # If ties, prefer earlier lines (stable sort)
        candidates.sort(key=lambda x: x[0], reverse=True)
        
        best_dist, best_line = candidates[0]
        
        # Place it
        if best_line not in final_placements:
            final_placements[best_line] = []
        
        final_placements[best_line].append(person['cmd'])
        placed_lines.append(best_line)
        
        print(f" + Placing {fname} at Line {best_line} (Dist: {best_dist}, Mentions: {len(mentions)})")
    # Step 4: Reconstruct File
    final_lines = []
    for i, line in enumerate(content_lines_without_portraits):
        # Insert margin note AT THE END of the line? Or after the name?
        # Appending to end is safest for LaTeX (avoids breaking words)
        # But for margin placement, right after the name is best.
        # Let's just append to line for now to avoid complexity.
        
        text = line.rstrip()
        
        if i in final_placements:
            for cmd in final_placements[i]:
                text += cmd
                
        final_lines.append(text + "\n")

    with open(file_path, "w") as f:
        f.writelines(final_lines)
    print("Smart Layout Refinement complete.")

if __name__ == "__main__":
    refine_layout_file("/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex")

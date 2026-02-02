
import re
import os

def cleanup_chapter():
    file_path = "/Users/davidlary/Dropbox/Apps/Overleaf/MachineLearningBook/Chapter-Introduction.tex"
    
    with open(file_path, 'r') as f:
        content = f.read()
        
    print(f"Original length: {len(content)}")
    
    # 1. Remove Spurious Citations after \end{figure}
    # Pattern: \end{figure} \citep{...} or \end{figure}\citep{...}
    # We replace with just \end{figure}
    content = re.sub(r'\\end{figure}\s*\\citep{[^}]+}', r'\\end{figure}', content)
    
    # 2. Strip Massive Italics
    # Pattern: \textit{Paragraph...}
    # This is tricky because of nested braces.
    # Heuristic: If \textit{ starts a line and ends a line (approx), remove it.
    # Or just replace specific known blocks from the "bad" file view.
    # Changing "\textit{Machine learning...}" to "Machine learning..."
    
    # We'll use a loop to strip outer \textit{ if it wraps a large block (>50 chars)
    # Regex: \\textit\{(.*?)\} -> \1 (Non-greedy?)
    # Be careful not to strip short italics like \textit{Supervised learning} which are valid labels.
    # The bad ones seem to span multiple lines or start paragraphs.
    
    def strip_long_italics(match):
        inner = match.group(1)
        if len(inner) > 100: # Arbitrary threshold for "Massive block"
             return inner
        return match.group(0)
    
    # Simple regex for single-paragraph \textit
    # Note: re.DOTALL is needed if it spans lines.
    # But nested braces match is hard in regex.
    # Let's target the specific known bad start/ends if possible, or use a stack.
    # Given the file content, it looks like `\textit{Text...}` 
    
    # Strategy: Replace specific known error patterns identified in diagnosis
    # "\textit{Machine learning models are powerful..."
    
    bad_prefixes = [
        r'\\textit{Machine learning models are powerful',
        r'\\textit{The bias-variance tradeoff can be understood',
        r'\\textit{Overfitting occurs when',
        r'\\textit{The historical development',
        r'\\textit{Addressing the bias-variance',
        r'\\textit{In summary, the bias-variance'
    ]
    
    for prefix in bad_prefixes:
        # We replace "\textit{" with "" if it matches the start logic, 
        # and we need to find the closing brace... that's the hard part.
        pass
    
    # BETTER APPROACH: Just remove the specific `\textit{` and the TRAILING `}` 
    # if we can identify line ranges? No, line numbers shift.
    
    # Let's try a heuristic replacement for the known text blocks.
    # We know the content.
    content = content.replace(r'\textit{Machine learning models are powerful', 'Machine learning models are powerful')
    content = content.replace(r'\textit{The bias-variance tradeoff can be understood', 'The bias-variance tradeoff can be understood')
    content = content.replace(r'\textit{Overfitting occurs when', 'Overfitting occurs when')
    content = content.replace(r'\textit{The historical development', 'The historical development')
    content = content.replace(r'\textit{Addressing the bias-variance', 'Addressing the bias-variance')
    content = content.replace(r'\textit{In summary, the bias-variance', 'In summary, the bias-variance')
    
    # Now we have lingering closing braces `}` at the end of these blocks.
    # This is risky. "unseen data.}" -> "unseen data."
    content = content.replace('unseen data.}', 'unseen data.')
    content = content.replace('by any model.}', 'by any model.')
    content = content.replace('increase the other.}', 'increase the other.')
    content = content.replace('complex and expressive.}', 'complex and expressive.')
    content = content.replace('of neural networks.}', 'of neural networks.')
    
    # 3. Add \clearpage at end
    if "\\clearpage" not in content[-50:]:
        content += "\n\n\\clearpage\n"
        
    # 4. Fix Float Positions [h] -> [htbp]
    content = content.replace(r'\begin{figure}[h]', r'\begin{figure}[htbp]')
    
    with open(file_path, 'w') as f:
        f.write(content)
        
    print("Cleanup complete.")

if __name__ == "__main__":
    cleanup_chapter()

import { useState, useCallback } from "react";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";
import { Box, Paper, Menu, MenuItem } from "@mui/material";
import { debounce } from "lodash";

interface SpellCheckError {
  word: string;
  suggestions: string[];
  index: [number, number];
}

interface SpellCheckRange {
  index: number;
  length: number;
  word: string;
  suggestions: string[];
}

const AmharicEditor = () => {
  const [content, setContent] = useState("");
  const [errors, setErrors] = useState<SpellCheckError[]>([]);
  const [ranges, setRanges] = useState<SpellCheckRange[]>([]);
  const [contextMenu, setContextMenu] = useState<{
    mouseX: number;
    mouseY: number;
    error?: SpellCheckError;
  } | null>(null);

  const modules = {
    toolbar: [
      [{ header: [1, 2, 3, false] }],
      ["bold", "italic", "underline"],
      [{ list: "ordered" }, { list: "bullet" }],
      ["clean"],
    ],
  };

  // Spell check when content changes
  const checkSpelling = useCallback(
    debounce(async (text: string) => {
      if (!text || text.trim() === "") {
        setErrors([]);
        setRanges([]);
        return;
      }
      try {
        console.log("Checking text:", text);
        const response = await fetch(
          "http://localhost:8000/api/check-spelling",
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, use_pos: true }),
          }
        );
        if (!response.ok) {
          throw new Error(`HTTP error status:${response.status}`);
        }
        const data = await response.json();
        setErrors(data.errors);
        setRanges(data.ranges);

        // Apply formatting to errors
        const quill = (
          document.querySelector(".ql-editor") as any
        )?.getEditor();
        if (quill) {
          // Remove existing formats
          quill.removeFormat(0, quill.getLength());

          // Apply new formats
          data.ranges.forEach((range: SpellCheckRange) => {
            quill.formatText(range.index, range.length, {
              color: "red",
              underline: true,
            });
          });
        }
      } catch (error) {
        console.error("Spell check error:", error);
      }
    }, 500),
    []
  );

  // Handle content changes
  const handleChange = (value: string) => {
    console.log("Content changed: ", value);
    setContent(value);
    const plainText = value.replace(/<[^>]*>/g, "");
    checkSpelling(plainText);
  };

  // Handle right-click on misspelled words
  const handleContextMenu = (event: React.MouseEvent) => {
    event.preventDefault();
    const range = ranges.find((r) => {
      const selection = window.getSelection();
      if (!selection?.toString()) return false;
      return selection.toString() === r.word;
    });

    if (range) {
      setContextMenu({
        mouseX: event.clientX,
        mouseY: event.clientY,
        error: errors.find((e) => e.word === range.word),
      });
    }
  };

  // Handle suggestion selection
  const handleSuggestionClick = async (suggestion: string) => {
    if (contextMenu?.error) {
      try {
        const response = await fetch("http://localhost:8000/api/replace-word", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            text: content,
            index: contextMenu.error.index[0],
            replacement: suggestion,
          }),
        });
        const data = await response.json();
        setContent(data.text);
        checkSpelling(data.text);
      } catch (error) {
        console.error("Replace word error:", error);
      }
    }
    setContextMenu(null);
  };
  const testSpellChecker = async () => {
    try {
      const testText = "ትማረ"; 
      console.log("Testing with text:", testText);

      const response = await fetch("http://localhost:8000/api/check-spelling", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: testText, use_pos: true }),
      });
      if (!response.ok){
        const errorText =await response.text();
        throw new Error (`HTTP error ! status :${response.status},message:${errorText}`)
      }

      const data = await response.json();
      console.log("Test response:", data);
    } catch (error) {
      console.error("Test error:", error);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 2, width: "100%", margin: "0 auto" }}>
      <Box
        sx={{
          minHeight: "400px",
          width: "100%",
          position: "relative",
        }}
        onContextMenu={handleContextMenu}
      >
        <button onClick={testSpellChecker} style={{ marginTop: "10px" }}>
          Test Spell Checker
        </button>
        <ReactQuill
          theme="snow"
          value={content}
          onChange={handleChange}
          modules={modules}
          placeholder="Start typing in Amharic..."
          style={{ height: "350px", width: "100%" }}
        />

        <Menu
          open={contextMenu !== null}
          onClose={() => setContextMenu(null)}
          anchorReference="anchorPosition"
          anchorPosition={
            contextMenu !== null
              ? { top: contextMenu.mouseY, left: contextMenu.mouseX }
              : undefined
          }
        >
          {contextMenu?.error?.suggestions.map((suggestion, index) => (
            <MenuItem
              key={index}
              onClick={() => handleSuggestionClick(suggestion)}
            >
              {suggestion}
            </MenuItem>
          ))}
        </Menu>
      </Box>
    </Paper>
  );
};

export default AmharicEditor;

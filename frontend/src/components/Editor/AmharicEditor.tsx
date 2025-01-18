import { useState } from "react";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css";

const AmharicEditor = () => {
  const [content, setContent] = useState("");

  const modules = {
    toolbar: [
      [{ header: [1, 2, 3, false] }],
      ["bold", "italic", "underline"],
      [{ list: "ordered" }, { list: "bullet" }],
      ["clean"],
    ],
  };

  const formats = ["header", "bold", "italic", "underline", "list", "bullet"];

  const handleChange = (value: string) => {
    setContent(value);
    console.log(value); // To debug
  };

  return (
    <div className="editor" style={{ width: "100%" }}>
      <ReactQuill
        theme="snow"
        value={content}
        onChange={handleChange}
        modules={modules}
        formats={formats}
        placeholder="Start typing in Amharic..."
        style={{ height: "350px", width: "100%" }}
      />
    </div>
  );
};

export default AmharicEditor;

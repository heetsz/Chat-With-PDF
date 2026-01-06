import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { uploadPDF } from '../lib/upload_pdf';
import { useNavigate } from "react-router-dom";

const Upload = () => {
      const [file, setFile] = useState(null);
      const navigate = useNavigate();

      async function handleUpload(){
            if(!file) alert("no file entered"); 
            try {
                  const data = await uploadPDF(file);
                  console.log(data);
                  navigate("/chat")
            } catch (err) {
                  console.error(err);
                  alert("Upload failed");
            }
      }
  return (
    <div>

      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />
      <Button onClick={handleUpload}>Upload PDF</Button>
    </div>
  )
}

export default Upload
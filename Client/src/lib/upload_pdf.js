import api from "@/lib/api";

export async function uploadPDF(file) {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post("/upload-pdf", formData, {
            headers: {
                  "Content-Type": "multipart/form-data",
            },
      });

      return response.data;
}

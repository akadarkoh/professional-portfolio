import { db } from "../../firebase/config";
import { addDoc, collection } from "firebase/firestore";

export default async function handler(req, res) {
  if (req.method === "POST") {
    await addDoc(collection(db, "comments"), {
      text: req.body.text,
      projectId: req.body.projectId,
      timestamp: new Date()
    });
    res.status(200).json({ success: true });
  }
}
import { db } from "../../firebase/config";
import { addDoc, collection } from "firebase/firestore";

export default async function handler(req, res) {
  if (req.method === "POST") {
    await addDoc(collection(db, "contacts"), {
      name: req.body.name,
      email: req.body.email,
      message: req.body.message,
      timestamp: new Date()
    });
    res.status(200).json({ success: true });
  }
}
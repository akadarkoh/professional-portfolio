import { db } from "../../firebase/config";
import { doc, increment, updateDoc } from "firebase/firestore";

export default async function handler(req, res) {
  if (req.method === "POST") {
    await updateDoc(doc(db, "projects", req.body.projectId), {
      views: increment(1)
    });
    res.status(200).json({ success: true });
  }
}
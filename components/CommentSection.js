import { useState } from "react";
import { db } from "../firebase/config";
import { collection, addDoc, query, where, onSnapshot } from "firebase/firestore";

export default function CommentSection({ projectId }) {
  const [comment, setComment] = useState("");
  const [comments, setComments] = useState([]);

  // Fetch comments for this project
  useEffect(() => {
    const q = query(collection(db, "comments"), where("projectId", "==", projectId));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      setComments(snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() })));
    });
    return unsubscribe;
  }, [projectId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addDoc(collection(db, "comments"), {
      text: comment,
      projectId,
      timestamp: new Date()
    });
    setComment("");
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input 
          value={comment} 
          onChange={(e) => setComment(e.target.value)} 
        />
        <button type="submit">Post</button>
      </form>
      <ul>
        {comments.map(c => (
          <li key={c.id}>{c.text}</li>
        ))}
      </ul>
    </div>
  );
}
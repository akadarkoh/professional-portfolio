import { db } from "../firebase/config";
import { doc, increment, updateDoc } from "firebase/firestore";

export default function ProjectCard({ project }) {
  const handleLike = async () => {
    await updateDoc(doc(db, "projects", project.id), {
      likes: increment(1)
    });
  };

  return (
    <div>
      <h2>{project.title}</h2>
      <p>{project.description}</p>
      <button onClick={handleLike}>Like ({project.likes || 0})</button>
    </div>
  );
}
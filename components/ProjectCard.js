// import { db } from "../firebase/config";
// import { doc, increment, updateDoc } from "firebase/firestore";

// export default function ProjectCard({ project }) {
//   const handleLike = async () => {
//     await updateDoc(doc(db, "projects", project.id), {
//       likes: increment(1)
//     });
//   };

//   return (
//     <div>
//       <h2>{project.title}</h2>
//       <p>{project.description}</p>
//       <button onClick={handleLike}>Like ({project.likes || 0})</button>
//     </div>
//   );
// }

// components/ProjectCard.js
import { doc, updateDoc, increment } from "firebase/firestore";
import { db } from "@/firebase/config";

export default function ProjectCard({ project }) {
  // Handle like action
  const handleLike = async () => {
    await updateDoc(doc(db, "projects", project.id), {
      likes: increment(1) // Increments "likes" in Firestore
    });
  };

  return (
    <div className="project-card">
      <h3>{project.title}</h3>
      <p>{project.description}</p>
      
      {/* Like Button */}
      <button onClick={handleLike}>
        ❤️ Likes: {project.likes || 0}
      </button>
    </div>
  );
}
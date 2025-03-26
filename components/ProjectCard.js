import { doc, updateDoc, increment } from 'firebase/firestore';
import { db } from '../firebase/config';

export default function ProjectCard({ project }) {
  const handleLike = async () => {
    await updateDoc(doc(db, 'projects', project.id), {
      likes: increment(1)
    });
  };

  return (
    <div className="project-card">
      <h3>{project.title}</h3>
      <p>{project.description}</p>
      
      {/* GitHub Badge */}
      {project.isGitHub && (
        <div className="github-badge">
          ⭐ {project.stars} | <a href={project.url}>GitHub</a>
        </div>
      )}
      
      {/* Like Button */}
      <button onClick={handleLike}>
        ❤️ Likes: {project.likes || 0}
      </button>
    </div>
  );
}
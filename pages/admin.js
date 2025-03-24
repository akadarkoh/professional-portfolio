import { auth, db } from "../firebase/config";
import { useAuthState } from "react-firebase-hooks/auth";
import { collection, addDoc } from "firebase/firestore";
import { signInWithGoogle } from "../firebase/auth";

export default function Admin() {
  const [user] = useAuthState(auth);
  const [project, setProject] = useState({ title: "", tags: [] });

  if (!user) return <button onClick={signInWithGoogle}>Login with Google</button>;

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addDoc(collection(db, "projects"), project);
    setProject({ title: "", tags: [] });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Title"
        value={project.title}
        onChange={(e) => setProject({ ...project, title: e.target.value })}
      />
      <input
        placeholder="Tags (comma-separated)"
        value={project.tags.join(",")}
        onChange={(e) => setProject({ ...project, tags: e.target.value.split(",") })}
      />
      <button type="submit">Add Project</button>
    </form>
  );
}
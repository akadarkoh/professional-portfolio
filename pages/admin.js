import { auth, db } from "../firebase/config";
import { useAuthState } from "react-firebase-hooks/auth";
import { collection, addDoc } from "firebase/firestore";
import { signInWithGoogle } from "../firebase/auth";
import { useState } from 'react';

export default function Admin() {
  const [user] = useAuthState(auth);
  const [project, setProject] = useState({ title: "", tags: [] });
  const [isSyncing, setIsSyncing] = useState(false);

  if (!user) return <button onClick={signInWithGoogle}>Login with Google</button>;

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addDoc(collection(db, "projects"), project);
    setProject({ title: "", tags: [] });
  };

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      const res = await fetch('/api/sync-github', { method: 'POST' });
      if (!res.ok) throw new Error('Sync failed');
      alert('GitHub projects synced!');
    } catch (error) {
      alert(error.message);
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <div>
      <div>
        <button 
          onClick={handleSync}
          disabled={isSyncing}
          className="sync-button"
        >
          {isSyncing ? 'Syncing...' : 'Sync GitHub Projects'}
        </button>
      </div>

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
    </div>
  );
}
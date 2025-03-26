// pages/index.js
import { db } from "../firebase/config";
import { collection, getDocs } from "firebase/firestore";
import { useState, useEffect } from "react";
import ProjectCard from "../components/ProjectCard";
import { githubProjects } from '../data/projects'; // GitHub projects

export async function getStaticProps() {
  // Fetch Firebase projects at build time
  const projectsSnapshot = await getDocs(collection(db, "projects"));
  const firestoreProjects = projectsSnapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
  
  return { 
    props: { 
      firestoreProjects,
      githubProjects // Pass GitHub projects as prop
    } 
  };
}

export default function Home({ firestoreProjects, githubProjects }) {
  const [filter, setFilter] = useState("All");
  const [allProjects, setAllProjects] = useState([]);

  // Combine Firebase and GitHub projects on client side
  useEffect(() => {
    setAllProjects([...firestoreProjects, ...githubProjects]);
  }, [firestoreProjects, githubProjects]);

  const filteredProjects = filter === "All" 
    ? allProjects 
    : allProjects.filter(p => p.tags?.includes(filter)); // Optional chaining in case tags missing

  return (
    <div>
      <select onChange={(e) => setFilter(e.target.value)}>
        <option value="All">All</option>
        <option value="React">React</option>
        <option value="Node.js">Node.js</option>
      </select>
      
      {filteredProjects.map(project => (
        <ProjectCard key={project.id || project.title} project={project} />
      ))}
    </div>
  );
}
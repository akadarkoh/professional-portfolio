import { db } from "../firebase/config";
import { collection, getDocs } from "firebase/firestore";
import { useState } from "react";
import ProjectCard from "../components/ProjectCard";

export async function getStaticProps() {
  const projectsSnapshot = await getDocs(collection(db, "projects"));
  const projects = projectsSnapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data()
  }));
  return { props: { projects } };
}

export default function Home({ projects }) {
  const [filter, setFilter] = useState("All");

  const filteredProjects = filter === "All" 
    ? projects 
    : projects.filter(p => p.tags.includes(filter));

  return (
    <div>
      <select onChange={(e) => setFilter(e.target.value)}>
        <option value="All">All</option>
        <option value="React">React</option>
        <option value="Node.js">Node.js</option>
      </select>
      
      {filteredProjects.map(project => (
        <ProjectCard key={project.id} project={project} />
      ))}
    </div>
  );
}
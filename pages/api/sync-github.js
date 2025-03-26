import { db } from '../../../firebase/config';
import { doc, setDoc } from 'firebase/firestore';

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).end();

  try {
    // Fetch from GitHub API
    const response = await fetch('https://api.github.com/users/akadarkoh/repos', {
      headers: { Authorization: `token ${process.env.GITHUB_TOKEN}` }
    });
    const repos = await response.json();

    // Sync to Firestore
    await Promise.all(repos.map(repo => 
      setDoc(doc(db, 'projects', `gh-${repo.id}`), {
        title: repo.name,
        description: repo.description,
        url: repo.html_url,
        stars: repo.stargazers_count,
        isGitHub: true,
        likes: 0 // Initialize
      }, { merge: true })
    ));

    res.status(200).json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
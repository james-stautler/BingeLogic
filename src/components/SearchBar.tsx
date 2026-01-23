import styles from "../styles/SearchBar.module.css"

import { useState } from "react";
import { useRouter } from 'next/navigation';

interface SearchBarProps {
    onSearch: (query:String) => void;
}

export default function SearchBar() {
    
    const [query, setQuery] = useState('');
    const [error, setError] = useState(false);
    const router = useRouter();

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        // This should be a lightweight validation query prior to redirecting to a stats page where the actual heavy lifting is done
        // const results = await backend(query);
        // if the results are valid, push to the next page with the query and then do heavy lifting
        // router.push();
        // else show error here
        setError(true);
    }

    return (
        <div>
            <form className={styles.SearchBarContainer} onSubmit={handleSearch}>
                <input 
                    type="text" 
                    placeholder="Enter TV show" 
                    className={styles.SearchInput}
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                />
                <button type="submit" className={styles.SearchSubmit}>
                    🔍
                </button>
            </form>
            <div className={`${styles.ErrorText} ${error ? styles.visible : ''}`}>
                Your Query: {query}
            </div>
        </div>
    );
}

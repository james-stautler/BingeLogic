import styles from "../styles/SearchBar.module.css"

import { useState } from "react";
import { useRouter } from 'next/navigation';
import { useEffect } from "react";

interface SearchBarProps {
    onSearch: (query:String) => void;
}

interface SearchResult {
    tmdb_id: number,
    title: string,
    poster_path: string,
    release_date: string
}

async function getSuggestions(query:String) {
    try {
        const response = await fetch(`https://bingelogic-backend.onrender.com/api/suggestions?query=${query}`);

        if (!response.ok) {
            throw new Error(`HTTP error status: ${response.status}`); 
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Could not get suggestions: ", error);
    }
}

export default function SearchBar() {
    
    const [query, setQuery] = useState('');
    const [debouncedQuery, setDebouncedQuery] = useState('');
    const [suggestions, setSuggestions] = useState<SearchResult[]>([]);

    const [error, setError] = useState(false);
    const router = useRouter();
    
    useEffect(() => {
        const handler = setTimeout(() => {
            setDebouncedQuery(query);
        }, 500);

        return () => {
            clearTimeout(handler);
        };
    }, [query]);

    useEffect(() => {
        const fetchResults = async () => {

            if (!debouncedQuery) {
                setSuggestions([]);
                return;
            }

            const queryResults = await getSuggestions(debouncedQuery);
            
            if (queryResults) {
                const search_results: SearchResult[] = queryResults.map((item: any) => ({
                    tmdb_id: item.tmdb_id,
                    title: item.title,
                    poster_path: item.poster_path,
                    release_date: item.release_date
                }));

                setSuggestions(search_results); 
            }
        };

        fetchResults();

    }, [debouncedQuery]);
    

    const handleSearch = async (e: React.FormEvent) => {
        e.preventDefault();
        setError(true);
    }

    if (suggestions.length != 0) {
        console.log(suggestions);
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

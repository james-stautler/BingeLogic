"use client";

import styles from "../styles/SearchBar.module.css"

import { useState } from "react";
import { useRouter } from 'next/navigation';
import { useEffect } from "react";
import Link from "next/link";

const SUGGESTION_LIMIT = 4;
const POSTER_QUERY_URL = "https://image.tmdb.org/t/p/w92"

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

export default function SearchBar({navBar} : {navBar : boolean}) { 
    
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

            if (!debouncedQuery || debouncedQuery.length < 2) {
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

                setSuggestions(search_results.splice(0, SUGGESTION_LIMIT)); 
            }
            else {
                setSuggestions([]);
            }
        };

        fetchResults();

    }, [debouncedQuery]);
    

    const handleSearch = async (e: React.FormEvent) => {

        e.preventDefault();

        if (query.length < 2) {
            return;
        } 

        const queryResults = await getSuggestions(query); 
        
        if (queryResults) {

            const search_results: SearchResult[] = queryResults.map((item: any) => ({
                    tmdb_id: item.tmdb_id,
                    title: item.title,
                    poster_path: item.poster_path,
                    release_date: item.release_date
            }));  
            
            if (search_results) {
                const result = search_results[0];
                router.push("/show-metrics?query=" + result.tmdb_id); 
            }
        }
    }

    if (suggestions.length != 0) {
        console.log(suggestions);
    }

    return (
        <div>
            <div className={styles.SearchBarContainer}>
                <form onSubmit={handleSearch}>
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
            </div>
            <div className={`${styles.SuggestionDropdownContainer} ${(suggestions.length > 0 && !navBar) ? styles.visible : ''}`}>
                 {suggestions.map((show) => (
                    <Link href={"/show-metrics?query=" + show.tmdb_id} key={show.tmdb_id} className={styles.SuggestionDropdownItem}>
                        <div className={styles.SuggestionDropdownLeft}>
                            <div className={styles.SuggestionPoster}>
                                <img src={POSTER_QUERY_URL + show.poster_path}/>
                            </div>
                            <div className={styles.SuggestionDropdownMeta}>
                                <div className={styles.SuggestionDropdownTitle}>
                                    {show.title}
                                </div>
                                <div className={styles.SuggestionDropdownDate}>
                                    {show.release_date.slice(0, 4)}
                                </div>
                            </div>
                        </div>
                        <div className={styles.SuggestionDropdownRight}>
                            &rarr;
                        </div>
                    </Link>
                ))}
            </div>
        </div>
    );
}

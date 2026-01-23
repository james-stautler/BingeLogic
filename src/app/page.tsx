"use client"

import styles from "../styles/Home.module.css"

import SearchBar from "../components/SearchBar"

export default function Home() {
    return (
        <div className={styles.HomeContainer}>
            <div className={styles.HeaderContainer}>
                <div className={styles.HeaderTitle}>
                    BingeLogic
                </div>
                <div className={styles.HeaderSubtitle}>
                   Quantifying the art of the binge. 
                </div>
                <SearchBar/>
            </div>
        </div>
    )
}

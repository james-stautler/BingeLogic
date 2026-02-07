import styles from "styles/Loading.module.css"
import LOADING_GIF from "public/loading.gif"
import Image from "next/image"

export default function Loading() {
    return (
        
        <div className={styles.LoadingContainer}>
            <Image
                src={LOADING_GIF}
                alt={"Loading GIF..."}
                width={256}
                height={256}
                unoptimized
                priority
            />
            <div className={styles.LoadingText}>
                Computing Binge Metrics... 
            </div>
            <div className={styles.LoadingSubtext}>
                Requests can take up to ~1 minute on initial server startup, I'm on free tier hosting.
            </div>
        </div>
    )
}

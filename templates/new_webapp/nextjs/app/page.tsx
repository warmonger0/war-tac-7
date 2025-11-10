'use client'

import { useState } from 'react'
import styles from './page.module.css'

export default function Home() {
  const [count, setCount] = useState(0)

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>Welcome to Your App</h1>
        <p className={styles.description}>
          Built with Next.js + TypeScript + App Router
        </p>

        <div className={styles.card}>
          <button
            onClick={() => setCount((count) => count + 1)}
            className={styles.button}
          >
            count is {count}
          </button>
          <p className={styles.hint}>
            Edit <code>app/page.tsx</code> and save to reload
          </p>
        </div>

        <p className={styles.footer}>
          Ready for ADW-powered feature development
        </p>
      </div>
    </main>
  )
}

import {create} from 'zustand'
import type {Difficulty, AudioFeatures, GuessResponse, RevealResponse} from '../types/game'
import {api} from '../api/client'

interface GameStore {
    sessionId: string | null
    difficulty: Difficulty | null
    hintsRemaining: number
    features: AudioFeatures | null
    categories: string[]
    result: GuessResponse | null
    reveal: RevealResponse | null
    loading: boolean
    error: string | null

    startSession: (difficulty: Difficulty) => Promise<void>
    useHint: () => Promise<void>
    submitGuess: (answer: string) => Promise<void>
    fetchReveal: () => Promise<void>
    fetchCategories: () => Promise<void>
    reset: () => void
}

const initialState = {
    sessionId: null,
    difficulty: null,
    hintsRemaining: 0,
    features: null,
    categories: [],
    result: null,
    reveal: null,
    loading: false,
    error: null,
}

function mergeFeatures(existing: AudioFeatures, incoming: AudioFeatures): AudioFeatures {
    const mergeGroup = <T extends object>(base: T, update: T): T => ({
        ...base,
        ...Object.fromEntries(Object.entries(update).filter(([, v]) => v !== null)),
    })
    return {
        time_domain: mergeGroup(existing.time_domain, incoming.time_domain),
        spectral: mergeGroup(existing.spectral, incoming.spectral),
        perceptual: mergeGroup(existing.perceptual, incoming.perceptual),
        rhythm: mergeGroup(existing.rhythm, incoming.rhythm),
        quality: mergeGroup(existing.quality, incoming.quality),
    }
}

export const useGameStore = create<GameStore>((set, get) => ({
    ...initialState,

    startSession: async (difficulty) => {
        set({loading: true, error: null})
        try {
            console.log("Callling session")
            const res = await api.startSession(difficulty)
            set({
                sessionId: res.session_id,
                difficulty: res.difficulty,
                hintsRemaining: res.hints_remaining,
                features: res.features,
                loading: false,
            })
            console.log("Got Session", res)
        } catch (e: any) {
            set({error: e.message, loading: false})
        }
    },

    useHint: async () => {
        const {sessionId, features} = get()
        if (!sessionId || !features) return
        set({loading: true, error: null})
        try {
            const res = await api.useHint(sessionId)
            set({
                hintsRemaining: res.hints_remaining,
                features: mergeFeatures(features, res.features),
                loading: false,
            })
        } catch (e: any) {
            set({error: e.message, loading: false})
        }
    },

    submitGuess: async (answer) => {
        const {sessionId} = get()
        if (!sessionId) return
        set({loading: true, error: null})
        try {
            const res = await api.submitGuess(sessionId, answer)
            set({result: res, loading: false})
            // fetch reveal immediately after guess
            const revealRes = await api.reveal(get().sessionId!)
            set({reveal: revealRes})
        } catch (e: any) {
            set({error: e.message, loading: false})
        }
    },

    fetchReveal: async () => {
        const {sessionId} = get()
        if (!sessionId) return
        set({loading: true, error: null})
        try {
            const res = await api.reveal(sessionId)
            set({reveal: res, loading: false})
        } catch (e: any) {
            set({error: e.message, loading: false})
        }
    },

    fetchCategories: async () => {
        try {
            const res = await api.getCategories()
            console.log("Categories", res)
            set({categories: res})
        } catch (e: any) {
            set({error: e.message})
        }
    },

    reset: () => set(initialState),
}))

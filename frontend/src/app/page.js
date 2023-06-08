'use client'
import axios from 'axios'
import Image from 'next/image'
import { useState, useEffect } from 'react'

export default function Home() {
  const [puerta, setPuerta] = useState(false);
  const [led, setLed] = useState(false)
  const url = process.env.NEXT_PUBLIC_ENDPOINT;

  const toggleDoor = async () => {
    console.log("changing door status")
    
      const response = await axios.get(`${url}/door`)
      setPuerta(response.data.status)
    
  }

  const toggleLamp = async () => {
    console.log("Changing lamp status")
    
      const response = await axios.get(`${url}/led`)
      setPuerta(response.data.status)
    
  }

  useEffect(() => {
    console.log("effect is working")
    const getDoorStatus = async () => {
      const response = await axios.get(`${url}/door/status`)
      setPuerta(response.data.status)
    }
    const getLedStatus = async () => {
      const response = await axios.get(`${url}/led/status`)
      setLed(response.data.status)
    }
    getDoorStatus()
    getLedStatus()

  }, [puerta,led])

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <button onClick={toggleDoor} className={puerta ? 'bg-green-500 ' : 'bg-red-500 ' + 'hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'}>Puerta {puerta ? 'Abierta' : 'Cerrada'}</button>
      <button onClick={toggleLamp} className={led ? 'bg-green-500 ' : 'bg-red-500 ' + 'hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'}>LED {led ? 'Encendido' : 'Apagado'}</button>
      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px]">
        <Image
          className="relative dark:drop-shadow-[0_0_0.3rem_#ffffff70] dark:invert"
          src="/next.svg"
          alt="Next.js Logo"
          width={180}
          height={37}
          priority
        />
      </div>
    </main>
  )
}

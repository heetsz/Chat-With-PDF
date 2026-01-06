import React from 'react'
import { Routes, Route } from 'react-router-dom'
import Upload from '@/pages/Upload'
import Chatbot from './pages/Chatbot'

const App = () => {
  return (
    <Routes>
      <Route path='/' element={<Upload/>} />
      <Route path='/chat' element={<Chatbot/>} />
    </Routes>
  )
}

export default App
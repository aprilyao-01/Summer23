import React from 'react'
import Emoji from './Emoji'

const HeadTitle = () => {
  return (
    <div>
        <h1>Fake Company</h1>
        <h2>
          Since summer 2023
          <Emoji symbol='🤓' label='wise-face' />
        </h2>
        
        <h2>
          Looking for partners
          <Emoji symbol= '🤝' label='shake-hand' />
        </h2>
    </div>
  )
}

export default HeadTitle
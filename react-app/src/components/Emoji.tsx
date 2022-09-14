import React from 'react'

interface EmojiProps {
    symbol: React.AriaRole,
    label?: string
}

const Emoji : React.FC<EmojiProps> = props => {
  return (
    <span
        className="emoji"
        role="img"
        aria-label={props.label ? props.label : ""}
        aria-hidden={props.label ? "false" : "true"} >
        {props.symbol}
    </span>
  )
}

export default Emoji
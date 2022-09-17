import React, { useState } from 'react'
import App from '../App';
import AntDesign from './AntDesign';
import { Switch } from 'antd';

const IsAnt = () => {
    const [isAnt, setAnt] = useState<boolean>(false);

    const handleSwitch = () => {
        setAnt(!isAnt);
    }

    return (
        <div>
            {/* <Switch checkedChildren="Customize UI" unCheckedChildren="Ant UI" 
                onClick={handleSwitch} className='switch' defaultChecked/> */}
            {isAnt? <AntDesign /> : <App/>}
        </div>
        
    )
}

export default IsAnt
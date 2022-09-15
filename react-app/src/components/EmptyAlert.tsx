import React, { useEffect, useRef, useState } from 'react'

const EmptyAlert = ({isEmpty}: {isEmpty: boolean}) => {
    const alertRef = useRef<HTMLParagraphElement>(null);
    console.log('isEmpty in EmptyAlert ' + isEmpty);
    const [countdown, setCountDown] = useState<number>(5);

    useEffect(() => {
        console.log("countdown" + countdown);
        const timer = setTimeout(() => {     // disappear after 2s
            // alertRef.current?.remove();
            setCountDown(0);
        }, 2000);
        return () => clearTimeout(timer);
      }, [isEmpty]);

    return (
    isEmpty ? (<p id='alert' ref={alertRef} >Please insert the employee name </p>) : (null)
    )
}
export default EmptyAlert

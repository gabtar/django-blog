import React from 'react';
import './Modal.css';
import '../assets/styles.css'

function Modal({show, setShow, children }) {

  return (
    <div className='modal' style={{display: show ? 'block' : 'none' }}>
      <div className='modal-container'>
        {children}
        <button className='btn exit-btn' onClick={() => setShow(false) }>
          &#10006;
        </button>
      </div>
    </div>
  )
}

export default Modal;

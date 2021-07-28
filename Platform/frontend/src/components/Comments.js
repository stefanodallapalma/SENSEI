// This section creates the comment section. More specifically, it defines the 'commentbox' extension
// Import necessary packages and scripts
import React, { Component,useEffect, useState } from 'react';
import commentBox from 'commentbox.io';


// Define the function that will be exported
function Comments() {
  // Define useStates
    const [open, setOpen] = useState(true);

    useEffect(() => {
        var comment = commentBox('5753003650842624-proj')
    
      }, []);

      const handleClose = (event) => {
    
        setOpen(false);
        
      };
    
    

    return(
        <div className="try">
            <div className="commentbox" />

        </div>
        
    )
};

export default Comments
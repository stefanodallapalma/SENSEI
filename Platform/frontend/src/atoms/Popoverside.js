// This script creates the information section for the knowledge page
// Import necessary packages and scripts
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Popper from '@material-ui/core/Popper';
import Typography from '@material-ui/core/Typography';
import HelpOutlineIcon from '@material-ui/icons/HelpOutline';
import { IconButton } from '@material-ui/core';
import Fade from '@material-ui/core/Fade';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles((theme) => ({
  typography: {
    padding: theme.spacing(2),
  },
}));


// Create export function
export default function SimplePopover(props) {

    // Define useStates
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [open, setOpen] = React.useState(false);
    const [placement, setPlacement] = React.useState();
    const classes = useStyles();
  
    const handleClick = (newPlacement) => (event) => {
      setAnchorEl(event.currentTarget);
      setOpen((prev) => placement !== newPlacement || !prev);
      setPlacement(newPlacement);
    };

  

  return (
    <div>
        <IconButton  variant="contained" color="primary" onClick={handleClick('right-start')} >
              <HelpOutlineIcon />
              </IconButton>
              <Popper open={open} anchorEl={anchorEl} placement={placement} transition>
        {({ TransitionProps }) => (
          <Fade {...TransitionProps} timeout={600}>
            <Paper>
              <Typography className="sidepopover">
                  This mindmap is a digital tool to map your thoughts regarding your specific investigation.
                  This notepad can aid in an analysis and its discussion with peers.
                    <br></br>
                    <br></br>
                  With the add functionality you can drag new nodes to the mindmap. For every research question (blue)
                  multiple hypotheses (black) can be added, which can be supported by arguments (pink). 
                  <br></br>
                  <br></br>
                  By clicking on a node you can alter its text and colour. The
                  nodes can be linked to each other by dragging a line between them.
                  <br></br>
                  <br></br>
                  You can delete a node by selecting it and pressing the 'backspace' key. 
                  <br></br>
                  <br></br>
                  To save the mindmap as pdf, you simple press the save button.
              </Typography>
            </Paper>
          </Fade>
        )}
      </Popper>
            
      
    </div>
  );
}
/* ==========================================================================
   Scripts for Header organism.
   ========================================================================== */


const Header = require( '../../organisms/Header.js' );
const header = new Header( document.body );
// Initialize header by passing it reference to global overlay atom.
header.init( document.body.querySelector( '.a-overlay' ) );

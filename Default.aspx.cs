using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;

namespace PokedexDatabaseProject
{
    public partial class _Default : Page
    {
        protected void Page_Load(object sender, EventArgs e)
        {
            //this is probably where we need to connect to the DB

        }

        //this is the handler for the serach button 
        protected void SearchBtn_Click(object sender, EventArgs e)
        {
            string query = QueryBox.Text; 

            //add the rest here for searching the database 
        }
    }
}
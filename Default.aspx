<%@ Page Title="Home Page" Language="C#" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="PokedexDatabaseProject._Default" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">

    <h1>PokeDex</h1>
    <br />
    <h3>This is a database of all Gen 1 Pokemon</h3>
    <br />
    <br />
    <h3>Search any of them here: </h3>
    <br />
    <asp:TextBox ID="QueryBox" runat="server"></asp:TextBox>
    <br />
    <asp:Button ID="SearchBtn" runat="server" Text="Search" />


</asp:Content>

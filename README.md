Simple project using micropython to read data from a gas reader (set up with ESP32), and a temperature reader (set up as a simulation on Wokwi), send that data to Supabase, and then display the readings (using Svelte)

Log in function uses an RFID reader to updated loggedIn status in Supabase.  This is then read by Svelte and allows a Member/User to log in.  Svelte contains a timeout function to log the user out after a certain period of inactivity

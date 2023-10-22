import React, { useState } from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';

export default function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false); // New state variable to track login status

  
  const handleLogin = () => {
    if(username && password) {
      const url = 'http://65.109.174.85:8080/token';
      // Constructing the URL-encoded body
      const body = new URLSearchParams();
      body.append('username', username);
      body.append('password', password);
      
      fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body.toString(), // Passing the URL-encoded body
      })
      .then((response) => {
        if (!response.ok) {
          return response.text().then((text) => {
            throw new Error(`Network response was not ok: ${text}`);
          });
        }
        return response.json();
      })
      .then((data) => {
        console.log('Success:', data);
        setIsLoggedIn(true); // Set to true on successful login
      })
      .catch((error) => {
        console.error('There was a problem with the fetch operation:', error);
      });
    } else {
      console.error('Username or Password is empty');
    }
  };
  return (
    <View style={styles.container}>
      {
        isLoggedIn ? (
          <Text style={styles.congratulationsText}>Congratulations!</Text>
        ) : (
          <View style={styles.loginBox}>
            <TextInput
              style={styles.input}
              placeholder="Username"
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
            />
            <TextInput
              style={styles.input}
              placeholder="Password"
              value={password}
              onChangeText={setPassword}
              secureTextEntry
              autoCapitalize="none"
            />
            <Button title="Accept" onPress={handleLogin} />
          </View>
        )
      }
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  loginBox: {
    width: '80%',
    padding: 20,
    backgroundColor: '#f9f9f9',
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 3,
  },
  input: {
    height: 40,
    borderBottomWidth: 1,
    marginBottom: 20,
  },
  congratulationsText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'green',
  },
});

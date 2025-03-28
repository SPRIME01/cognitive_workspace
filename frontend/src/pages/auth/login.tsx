import React, { useState } from 'react';
import { useRouter } from 'next/router';
import {
  Container,
  Typography,
  Box,
  TextField,
  Button,
  Paper,
  Link as MuiLink,
  Alert,
  CircularProgress
} from '@mui/material';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '@/contexts/auth';

export default function Login() {
  const router = useRouter();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err) {
      setError('Invalid email or password. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      <Head>
        <title>Login | Cognitive Workspace</title>
      </Head>

      <Container maxWidth="sm">
        <Box sx={{ mt: 8, mb: 4 }}>
          <Paper sx={{ p: 4, borderRadius: 2 }}>
            <Typography variant="h4" component="h1" align="center" gutterBottom>
              Log in to Cognitive Workspace
            </Typography>

            {error && (
              <Alert severity="error" sx={{ mb: 3 }}>
                {error}
              </Alert>
            )}

            <Box component="form" onSubmit={handleSubmit} noValidate>
              <TextField
                margin="normal"
                required
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isSubmitting}
              />
              <TextField
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type="password"
                id="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={isSubmitting}
              />

              <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2, py: 1.2 }}
                disabled={isSubmitting}
              >
                {isSubmitting ? <CircularProgress size={24} /> : 'Log In'}
              </Button>

              <Box sx={{ textAlign: 'center', mt: 2 }}>
                <Typography variant="body2">
                  Don't have an account?{' '}
                  <Link href="/auth/signup" passHref>
                    <MuiLink>Sign up</MuiLink>
                  </Link>
                </Typography>
                <Typography variant="body2" sx={{ mt: 1 }}>
                  <Link href="/auth/forgot-password" passHref>
                    <MuiLink>Forgot password?</MuiLink>
                  </Link>
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Box>
      </Container>
    </>
  );
}

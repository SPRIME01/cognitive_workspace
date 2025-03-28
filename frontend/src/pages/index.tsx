import React from 'react';
import Head from 'next/head';
import { Container, Typography, Box, Button, Grid } from '@mui/material';
import Link from 'next/link';
import Layout from '@/components/layout/Layout';
import { useAuth } from '@/contexts/auth';

export default function Home() {
  const { user } = useAuth();

  return (
    <Layout>
      <Head>
        <title>Cognitive Workspace</title>
        <meta name="description" content="A modern cognitive knowledge workspace" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <Typography variant="h2" component="h1" align="center" gutterBottom>
            Welcome to Cognitive Workspace
          </Typography>
          <Typography variant="h5" align="center" color="text.secondary" paragraph>
            Enhance your productivity with AI-assisted knowledge management
          </Typography>
          <Box sx={{ mt: 4 }}>
            <Grid container spacing={2} justifyContent="center">
              {user ? (
                <Grid item>
                  <Link href="/workspaces" passHref>
                    <Button variant="contained" color="primary">
                      Go to Workspaces
                    </Button>
                  </Link>
                </Grid>
              ) : (
                <>
                  <Grid item>
                    <Link href="/auth/signup" passHref>
                      <Button variant="contained" color="primary">
                        Sign Up
                      </Button>
                    </Link>
                  </Grid>
                  <Grid item>
                    <Link href="/auth/login" passHref>
                      <Button variant="outlined" color="primary">
                        Log In
                      </Button>
                    </Link>
                  </Grid>
                </>
              )}
            </Grid>
          </Box>
        </Box>

        <Box sx={{ my: 6 }}>
          <Grid container spacing={4}>
            <Grid item xs={12} md={4}>
              <Typography variant="h4" component="h2" gutterBottom>
                Organize
              </Typography>
              <Typography>
                Create workspaces to organize your knowledge. Categorize and tag information
                to make it easily accessible.
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h4" component="h2" gutterBottom>
                Collaborate
              </Typography>
              <Typography>
                Share workspaces with your team. Work together on documents and projects
                in real-time.
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h4" component="h2" gutterBottom>
                Analyze
              </Typography>
              <Typography>
                Leverage AI to analyze your data, extract insights, and make connections
                between different pieces of information.
              </Typography>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </Layout>
  );
}

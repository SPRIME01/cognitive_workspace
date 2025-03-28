import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import {
  Container,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  CardActionArea,
  Button,
  Divider,
  Chip,
  CircularProgress
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { useRouter } from 'next/router';
import Layout from '@/components/layout/Layout';
import { useAuth } from '@/contexts/auth';
import { Workspace } from '@shared/types';

export default function Dashboard() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading } = useAuth();
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [recentDocuments, setRecentDocuments] = useState([]);
  const [isLoadingData, setIsLoadingData] = useState(true);

  // Redirect if not authenticated
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Fetch workspace data
  useEffect(() => {
    const fetchData = async () => {
      if (isAuthenticated) {
        try {
          // In a real app, you would fetch this data from your API
          // Mock data for demonstration
          setTimeout(() => {
            setWorkspaces([
              {
                id: 'ws1',
                name: 'Research Projects',
                description: 'Workspace for ongoing research projects and notes',
                ownerId: 'user-123',
                isPublic: false,
                createdAt: '2023-06-01T00:00:00Z',
                updatedAt: '2023-06-15T00:00:00Z'
              },
              {
                id: 'ws2',
                name: 'Product Development',
                description: 'Ideas and plans for new product features',
                ownerId: 'user-123',
                isPublic: true,
                createdAt: '2023-05-20T00:00:00Z',
                updatedAt: '2023-06-20T00:00:00Z'
              },
              {
                id: 'ws3',
                name: 'Personal Notes',
                description: 'Personal thoughts and notes',
                ownerId: 'user-123',
                isPublic: false,
                createdAt: '2023-04-10T00:00:00Z',
                updatedAt: '2023-06-18T00:00:00Z'
              }
            ]);

            setRecentDocuments([
              {
                id: 'doc1',
                title: 'Project Roadmap',
                updatedAt: '2023-06-25T00:00:00Z',
                workspaceId: 'ws2'
              },
              {
                id: 'doc2',
                title: 'Research Findings',
                updatedAt: '2023-06-23T00:00:00Z',
                workspaceId: 'ws1'
              },
              {
                id: 'doc3',
                title: 'Meeting Notes',
                updatedAt: '2023-06-20T00:00:00Z',
                workspaceId: 'ws1'
              }
            ]);

            setIsLoadingData(false);
          }, 1000);
        } catch (error) {
          console.error('Error fetching dashboard data:', error);
          setIsLoadingData(false);
        }
      }
    };

    fetchData();
  }, [isAuthenticated]);

  if (isLoading || !isAuthenticated) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Layout>
      <Head>
        <title>Dashboard | Cognitive Workspace</title>
      </Head>

      <Container maxWidth="lg">
        <Box sx={{ py: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Welcome back, {user?.name || 'User'}
          </Typography>

          <Grid container spacing={4} sx={{ mt: 2 }}>
            {/* Recent Workspaces */}
            <Grid item xs={12} md={8}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h5" component="h2">
                  Your Workspaces
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => router.push('/workspaces/new')}
                >
                  New Workspace
                </Button>
              </Box>

              {isLoadingData ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <div className="workspace-grid">
                  {workspaces.map((workspace) => (
                    <Card key={workspace.id} className="card-hover" sx={{ height: '100%' }}>
                      <CardActionArea
                        onClick={() => router.push(`/workspaces/${workspace.id}`)}
                        sx={{ height: '100%' }}
                      >
                        <CardContent>
                          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                            <Typography variant="h6" component="h3" className="truncate">
                              {workspace.name}
                            </Typography>
                            {workspace.isPublic ? (
                              <Chip label="Public" size="small" color="primary" variant="outlined" />
                            ) : (
                              <Chip label="Private" size="small" color="default" variant="outlined" />
                            )}
                          </Box>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                            {workspace.description || 'No description'}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            Last updated:{' '}
                            {new Date(workspace.updatedAt).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric'
                            })}
                          </Typography>
                        </CardContent>
                      </CardActionArea>
                    </Card>
                  ))}
                </div>
              )}

              {!isLoadingData && workspaces.length === 0 && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <Typography variant="body1" color="text.secondary">
                    You don't have any workspaces yet.
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    onClick={() => router.push('/workspaces/new')}
                    sx={{ mt: 2 }}
                  >
                    Create Your First Workspace
                  </Button>
                </Box>
              )}
            </Grid>

            {/* Recent Activity / Documents */}
            <Grid item xs={12} md={4}>
              <Box sx={{ mb: 2 }}>
                <Typography variant="h5" component="h2">
                  Recent Activity
                </Typography>
              </Box>

              {isLoadingData ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
                  <CircularProgress />
                </Box>
              ) : (
                <Card>
                  <CardContent>
                    {recentDocuments.length > 0 ? (
                      <Box>
                        {recentDocuments.map((doc, index) => (
                          <React.Fragment key={doc.id}>
                            <Box
                              sx={{ py: 1.5, px: 1 }}
                              className="document-list-item"
                              onClick={() => router.push(`/documents/${doc.id}`)}
                            >
                              <Typography variant="body1" className="truncate">
                                {doc.title}
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {new Date(doc.updatedAt).toLocaleDateString('en-US', {
                                  year: 'numeric',
                                  month: 'short',
                                  day: 'numeric'
                                })}
                              </Typography>
                            </Box>
                            {index < recentDocuments.length - 1 && <Divider />}
                          </React.Fragment>
                        ))}
                      </Box>
                    ) : (
                      <Typography variant="body2" color="text.secondary" sx={{ py: 2, textAlign: 'center' }}>
                        No recent activity
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              )}
            </Grid>
          </Grid>
        </Box>
      </Container>
    </Layout>
  );
}

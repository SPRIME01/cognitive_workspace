import React from 'react';
import { useRouter } from 'next/router';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Box,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  IconButton
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Person as PersonIcon,
  Description as DocumentIcon,
  Folder as WorkspaceIcon,
  Settings as SettingsIcon,
  Logout as LogoutIcon
} from '@mui/icons-material';
import Link from 'next/link';
import { useAuth } from '@/contexts/auth';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, isAuthenticated, logout } = useAuth();
  const router = useRouter();
  const [drawerOpen, setDrawerOpen] = React.useState(false);

  const toggleDrawer = () => {
    setDrawerOpen(!drawerOpen);
  };

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          {isAuthenticated && (
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="menu"
              sx={{ mr: 2 }}
              onClick={toggleDrawer}
            >
              <MenuIcon />
            </IconButton>
          )}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            <Link href="/" passHref>
              <Box component="a" sx={{ color: 'inherit', textDecoration: 'none' }}>
                Cognitive Workspace
              </Box>
            </Link>
          </Typography>

          {isAuthenticated ? (
            <>
              <Typography variant="body1" sx={{ mr: 2 }}>
                {user?.name || user?.email}
              </Typography>
              <Button color="inherit" onClick={handleLogout}>
                Logout
              </Button>
            </>
          ) : (
            <>
              <Button color="inherit" component="a" href="/auth/login">
                Login
              </Button>
              <Button color="inherit" component="a" href="/auth/signup">
                Sign Up
              </Button>
            </>
          )}
        </Toolbar>
      </AppBar>

      {isAuthenticated && (
        <Drawer
          anchor="left"
          open={drawerOpen}
          onClose={toggleDrawer}
        >
          <Box
            sx={{ width: 250 }}
            role="presentation"
            onClick={toggleDrawer}
          >
            <List>
              <ListItem button component="a" href="/dashboard">
                <ListItemIcon>
                  <DashboardIcon />
                </ListItemIcon>
                <ListItemText primary="Dashboard" />
              </ListItem>
              <ListItem button component="a" href="/workspaces">
                <ListItemIcon>
                  <WorkspaceIcon />
                </ListItemIcon>
                <ListItemText primary="Workspaces" />
              </ListItem>
              <ListItem button component="a" href="/documents">
                <ListItemIcon>
                  <DocumentIcon />
                </ListItemIcon>
                <ListItemText primary="Documents" />
              </ListItem>
            </List>
            <Divider />
            <List>
              <ListItem button component="a" href="/profile">
                <ListItemIcon>
                  <PersonIcon />
                </ListItemIcon>
                <ListItemText primary="Profile" />
              </ListItem>
              <ListItem button component="a" href="/settings">
                <ListItemIcon>
                  <SettingsIcon />
                </ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItem>
              <ListItem button onClick={handleLogout}>
                <ListItemIcon>
                  <LogoutIcon />
                </ListItemIcon>
                <ListItemText primary="Logout" />
              </ListItem>
            </List>
          </Box>
        </Drawer>
      )}

      <Box component="main" sx={{ flexGrow: 1, py: 3 }}>
        {children}
      </Box>

      <Box
        component="footer"
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
          backgroundColor: (theme) =>
            theme.palette.mode === 'light'
              ? theme.palette.grey[200]
              : theme.palette.grey[800],
        }}
      >
        <Container maxWidth="lg">
          <Typography variant="body2" color="text.secondary" align="center">
            © {new Date().getFullYear()} Cognitive Workspace
          </Typography>
        </Container>
      </Box>
    </>
  );
};

export default Layout;

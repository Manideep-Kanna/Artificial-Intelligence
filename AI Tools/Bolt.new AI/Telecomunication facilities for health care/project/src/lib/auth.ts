import { atom } from 'jotai';
import { supabase } from './supabase';
import { toast } from 'sonner';

export type UserRole = 'patient' | 'doctor';

export type User = {
  id: string;
  email: string;
  role: UserRole;
  user_metadata?: {
    full_name?: string;
  };
};

export const userAtom = atom<User | null | undefined>(undefined);
export const isLoadingAtom = atom(true);

export async function signIn(email: string, password: string) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  
  if (error) throw error;
  return data;
}

export async function signUp(
  email: string, 
  password: string, 
  role: UserRole,
  profileData: any
) {
  try {
    const { data: authData, error: authError } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          role: role,
        }
      }
    });

    if (authError) throw authError;

    if (!authData.user) {
      throw new Error('Registration failed');
    }

    return authData;
  } catch (error: any) {
    if (error.message?.includes('Email confirmation')) {
      return { user: null, session: null };
    }
    throw error;
  }
}

export async function signOut() {
  const { error } = await supabase.auth.signOut();
  if (error) throw error;
}

export async function getCurrentUser() {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    if (!session) return null;
    
    const { data: { user }, error } = await supabase.auth.getUser();
    if (error) throw error;
    return user;
  } catch (error) {
    console.error('Get current user error:', error);
    return null;
  }
}

export async function updateUserProfile(userId: string, data: { full_name: string }) {
  const { error } = await supabase.auth.updateUser({
    data: { full_name: data.full_name }
  });
  
  if (error) throw error;
  return getCurrentUser();
}

export async function initializeAuth() {
  try {
    const { data: { session } } = await supabase.auth.getSession();
    return session?.user || null;
  } catch (error) {
    console.error('Initialize auth error:', error);
    return null;
  }
}

// Remove the auth state listener from here as we'll handle it in the AuthGuard
import React, { useEffect, useState } from 'react';
import { Calendar, Clock, User, MapPin } from 'lucide-react';
import { supabase } from '@/lib/supabase';
import { useAtom } from 'jotai';
import { userAtom } from '@/lib/auth';
import { format } from 'date-fns';
import { toast } from 'sonner';

type DoctorAppointment = {
  id: number;
  patient: {
    email: string;
    user_metadata: {
      full_name?: string;
    };
  };
  start_time: string;
  status: 'upcoming' | 'completed' | 'cancelled';
  location: string;
  notes: string;
  type: {
    name: string;
    duration: number;
    price: number;
  };
};

export function DoctorDashboard() {
  const [user] = useAtom(userAtom);
  const [appointments, setAppointments] = useState<DoctorAppointment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedDate, setSelectedDate] = useState<string>(
    format(new Date(), 'yyyy-MM-dd')
  );

  useEffect(() => {
    if (user) {
      loadAppointments();
    }
  }, [user, selectedDate]);

  async function loadAppointments() {
    try {
      const startOfDay = new Date(`${selectedDate}T00:00:00`);
      const endOfDay = new Date(`${selectedDate}T23:59:59`);

      const { data, error } = await supabase
        .from('appointments')
        .select(`
          id,
          patient:patient_id(
            email,
            user_metadata
          ),
          start_time,
          status,
          location,
          notes,
          type:appointment_type_id(
            name,
            duration,
            price
          )
        `)
        .eq('doctor_id', user?.id)
        .gte('start_time', startOfDay.toISOString())
        .lte('start_time', endOfDay.toISOString())
        .order('start_time');

      if (error) throw error;
      setAppointments(data || []);
    } catch (error) {
      console.error('Error loading appointments:', error);
      toast.error('Failed to load appointments');
    } finally {
      setIsLoading(false);
    }
  }

  async function handleUpdateStatus(appointmentId: number, status: 'completed' | 'cancelled') {
    try {
      const { error } = await supabase
        .from('appointments')
        .update({ status })
        .eq('id', appointmentId);

      if (error) throw error;
      toast.success(`Appointment marked as ${status}`);
      loadAppointments();
    } catch (error) {
      console.error('Error updating appointment:', error);
      toast.error('Failed to update appointment');
    }
  }

  if (isLoading) {
    return (
      <div className="flex h-[50vh] items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Doctor Dashboard</h1>
          <p className="mt-2 text-gray-600">Manage your appointments and patient schedule.</p>
        </div>
        <div>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="rounded-md border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
      </div>

      <div className="mt-8">
        <h2 className="text-xl font-semibold text-gray-900">Today's Appointments</h2>
        <div className="mt-4 space-y-6">
          {appointments.length === 0 ? (
            <div className="rounded-lg bg-white p-6 text-center shadow">
              <p className="text-gray-600">No appointments scheduled for this date.</p>
            </div>
          ) : (
            appointments.map((appointment) => (
              <div
                key={appointment.id}
                className="rounded-lg bg-white p-6 shadow"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {appointment.patient.user_metadata?.full_name || 'Patient'}
                    </h3>
                    <p className="text-gray-600">{appointment.patient.email}</p>
                    <p className="text-sm text-gray-500">{appointment.type.name}</p>
                  </div>
                  <span
                    className={`inline-flex rounded-full px-3 py-1 text-sm font-medium ${
                      appointment.status === 'upcoming'
                        ? 'bg-green-100 text-green-800'
                        : appointment.status === 'cancelled'
                        ? 'bg-red-100 text-red-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {appointment.status.charAt(0).toUpperCase() + appointment.status.slice(1)}
                  </span>
                </div>

                <div className="mt-4 grid gap-4 sm:grid-cols-3">
                  <div className="flex items-center">
                    <Clock className="h-5 w-5 text-gray-400" />
                    <span className="ml-2 text-gray-600">
                      {format(new Date(appointment.start_time), 'h:mm a')}
                    </span>
                  </div>
                  <div className="flex items-center">
                    <MapPin className="h-5 w-5 text-gray-400" />
                    <span className="ml-2 text-gray-600">{appointment.location}</span>
                  </div>
                  <div className="flex items-center">
                    <Calendar className="h-5 w-5 text-gray-400" />
                    <span className="ml-2 text-gray-600">
                      Duration: {appointment.type.duration} mins
                    </span>
                  </div>
                </div>

                {appointment.notes && (
                  <div className="mt-4">
                    <p className="text-sm text-gray-600">
                      <span className="font-medium">Notes:</span> {appointment.notes}
                    </p>
                  </div>
                )}

                {appointment.status === 'upcoming' && (
                  <div className="mt-6 flex space-x-4">
                    <button
                      onClick={() => handleUpdateStatus(appointment.id, 'completed')}
                      className="rounded-md bg-green-50 px-4 py-2 text-sm font-medium text-green-700 hover:bg-green-100"
                    >
                      Mark as Completed
                    </button>
                    <button
                      onClick={() => handleUpdateStatus(appointment.id, 'cancelled')}
                      className="rounded-md bg-red-50 px-4 py-2 text-sm font-medium text-red-700 hover:bg-red-100"
                    >
                      Cancel Appointment
                    </button>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
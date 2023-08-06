/*=========================================================================
 *
 *  Copyright RTK Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-2.0.txt
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *=========================================================================*/
#ifndef rtkGlobalTimer_h
#define rtkGlobalTimer_h

#include <itkProcessObject.h>
#include "rtkGlobalTimerProbesCollector.h"
#include "rtkTimeProbesCollectorBase.h"
#include "rtkWatcherForTimer.h"
#include "RTKExport.h"
#include <mutex>

namespace rtk
{
/** \class GlobalTimer
 * \brief
 *
 * \ingroup RTK OSSystemObjects
 * \ingroup RTK ITKCommon
 */

class RTK_EXPORT GlobalTimer:public itk::Object
{
public:
  ITK_DISALLOW_COPY_AND_ASSIGN(GlobalTimer);

  /** Standard class type alias. */
  using Self = GlobalTimer;
  using Superclass = itk::Object;
  using Pointer = itk::SmartPointer< Self >;
  using ConstPointer = itk::SmartPointer< const Self >;

  /** Run-time type information (and related methods). */
  itkTypeMacro(GlobalTimer, itk::Object)

  /** This is a singleton pattern New.  There will only be ONE
   * reference to a GlobalTimer object per process.  Clients that
   * call this must call Delete on the object so that the reference
   * counting will work.   The single instance will be unreferenced when
   * the program exits. */
  static Pointer New();

  /** Return the singleton instance with no reference counting. */
  static Pointer GetInstance();

  /** Set / Get macro for verbosity */
  itkSetMacro(Verbose, bool)
  itkGetMacro(Verbose, bool)

  /** Start a probe with a particular name. If the time probe does not
   * exist, it will be created */
  virtual void Start(const char *name);

  /** Stop a time probe identified with a name */
  virtual void Stop(const char *name);

  /** Report the summary of results from the probes */
  virtual void Report(std::ostream & os = std::cout) const;

  /** Destroy the set of probes. New probes can be created after invoking this
    method. */
  virtual void Clear(void);

  /** Create a new watcher and store it */
  virtual void Watch(itk::ProcessObject *o);

  /** Remove a watcher */
  virtual void Remove(const rtk::WatcherForTimer *w);

protected:
  GlobalTimer();
  ~GlobalTimer() override;
  void PrintSelf(std::ostream & os, Indent indent) const override;
  bool m_Verbose;

//  rtk::GlobalTimerProbesCollector m_GlobalTimerProbesCollector;
  rtk::TimeProbesCollectorBase       m_TimeProbesCollectorBase;
  std::vector<rtk::WatcherForTimer*> m_Watchers;

private:
  static Pointer m_Instance;
  std::mutex     m_Mutex;

};
} // end namespace itk

#endif

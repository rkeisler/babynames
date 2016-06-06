import numpy as np
import matplotlib.pylab as pl
pl.ion()
import matplotlib
matplotlib.rc('font', size=15)

'''
Example usage:

import names
x = names.Names()
x.viz('zelda')
x.viz('zelda jim noah')
x.viz_similar('zelda')

Similarity is based on the L1-distance between (log) popularity curves.
'''

class Names():

    def __init__(self, years=range(1900,2016)):
        self.data = {}
        self.grid_cnt = None
        self.load_data(years)
        self.build_cnt_grid()
        pl.close('all')
        pl.figure(1, figsize=(16,6))

    def load_data(self, years):
        out = {}
        for year in years:
            if (year % 10)==0: print year
            fname = 'data/yob%i.txt'%year
            x = np.loadtxt(fname, dtype='string', delimiter=',').T
            name, sex, cnt = x
            cnt = cnt.astype('float')
            for this_sex in ['F','M']:
                mask = sex==this_sex
                this_name = name[mask]
                this_cnt = cnt[mask]
                this_cnt /= np.sum(this_cnt)
                # sort
                ind = np.argsort(this_cnt)[::-1]
                this_name = this_name[ind]
                this_cnt = this_cnt[ind]
                rank = np.arange(len(this_cnt)) + 1
                for name_, cnt_, rank_ in zip(this_name, this_cnt, rank):
                    if name_ not in out:
                        out[name_] = {}
                    if year in out[name_]:
                        if out[name_][year]['rank'] < rank_: continue
                    out[name_][year] = {'rank':rank_, 
                                        'cnt':cnt_}
        self.data = out

    def build_cnt_grid(self, interp_years=range(1900,2016)):
        print '...building grid...'
        min_year = np.min(interp_years)
        max_year = np.max(interp_years)
        self.grid_cnt = []
        self.grid_names = []
        for name, v in self.data.iteritems():
            v = self.data[name]
            years = np.sort(v.keys())
            cnt = np.array([v[year]['cnt'] for year in years])
            # log(count) is a better metric.
            cnt = np.log(cnt)
            if min_year not in years:
                years = np.concatenate([[min_year], years])
                cnt = np.concatenate([[cnt[0]], cnt])
            if max_year not in years:
                years = np.concatenate([years, [max_year]])
                cnt = np.concatenate([cnt, [cnt[-1]]])
            interp_cnt = np.interp(interp_years, years, cnt)
            self.grid_cnt.append(interp_cnt)
            self.grid_names.append(name)
        self.grid_cnt = np.vstack(self.grid_cnt) # (n_names, n_years)
        self.grid_names = np.array(self.grid_names) # (n_names)
        self.grid_years = np.array(interp_years) # (n_years)

    def viz(self, names, title=None, lw=None,
            save=False, savename=None):
        '''
        NAMES can be
        a name: 'mary'
        space-separated names: 'mary james', or
        a list of names: ['mary','james'].
        Any capitalization works.
        '''
        pl.clf()
        leg = []
        colors = colorz()
        if isinstance(names, basestring):
            names = names.split()
        if lw is None: lw = 4.0 - 0.3*np.log(len(names))
        for iname,name_ in enumerate(names):
            name = name_.lower().capitalize()
            if name not in self.data:
                print '%s is not in database.'%name
                return
            leg.append(name)
            v = self.data[name]
            years = np.sort(v.keys())
            rank = np.array([v[year]['rank'] for year in years])
            cnt = np.array([v[year]['cnt'] for year in years])

            # rank
            pl.subplot(1,2,1)
            pl.semilogy(years, rank, '-', linewidth=lw, color=colors[iname])
            pl.ylabel('Rank')
            pl.ylim(1e5,1)
            pl.grid('on')

            # percentage
            pl.subplot(1,2,2)
            pl.semilogy(years, cnt*100, '-', linewidth=lw, color=colors[iname])
            pl.ylabel('Share (%)')
            pl.ylim(1e-4,10)
            pl.grid('on')

        # legend & title
        for i in [1,2]:
            pl.subplot(1,2,i)
            pl.legend(leg, loc='lower left', fontsize=11, framealpha=0.9)
            if title is not None:
                pl.title(title)
        pl.show()
        if save:
            if savename is None:
                savename = '%s.png'%('_'.join(names))
            print 'saving %s'%savename
            pl.savefig(savename)

    def similar_names(self, name_in, n=20, show=False):
        name = name_in.lower().capitalize()
        if name not in self.data:
            print '%s is not in database.'%name
            return []
        if self.grid_cnt is None:
            self.build_cnt_grid()
        this_cnt = self.grid_cnt[self.grid_names==name][0]
        dist = np.abs(self.grid_cnt - this_cnt).sum(1)
        ind = np.argsort(dist)[1:]
        snames = self.grid_names[ind[:n]]
        if show:
            print 'Names similar to %s:'%name.upper()
            for i in snames: print i
        return snames

    def viz_similar(self, name, n=20, lw=None, save=False):
        snames = self.similar_names(name, n=n)
        if len(snames)==0: return
        if save: savename='%s_similar%i.png'%(name, n)
        else: savename=None
        self.viz(snames, save=save, savename=savename, 
                 title='Similar to %s'%name.upper(), lw=lw)


def colorz():
    return 10*['#034f84','#f7786b','#009933','#cc0066','#50394c','#b2b2b2','#c94c4c','#618685','#4040a1','#563f46','#87bdd8','#e06377','#c83349','#ffcc5c','#b8a9c9','#ffeead','#96ceb4','#622569','#8ca3a3','#96897f']
    

def examples():
    x = Names()
    names = ['zelda','willard','jim','traci', 'geronimo','noah']
    for name in names:
        x.viz_similar(name, save=1)

        
if __name__ == '__main__':
    examples()
